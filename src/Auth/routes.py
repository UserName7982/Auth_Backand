from src.logger import logger
from fastapi import APIRouter, Depends, HTTPException,Query
from fastapi.responses import JSONResponse
from src.Mail import mail,create_message
from src.config import configs
from fastapi_limiter.depends import RateLimiter
from src.DB.Redis import add_to_blocklist
from src.Auth.utils import rl_callback
from datetime import datetime, timedelta
from src.Auth.Services import UserService, getSession
from src.celery_task import send_email
from urllib.parse import urlencode
from src.Auth.Schema import (Address,
                             CreateUser, 
                            LoginUser,User, 
                            passwordResetConfirm,
                            PassswordReset)
from src.Auth.utils import (create_url,
                            generate_password_hash,
                            verify_password_hash,
                            create_token,
                            decode_url)
from src.Auth.Dependancy import (AccessTokenBearer,
                                RefreshTokenBearer,
                                get_current_user,
                                RoleChecker,
                                custom_identifer)
role_che=Depends(RoleChecker(["admin","user"]))
ratelimiter=Depends(RateLimiter(times=5, seconds=60,
                                identifier=custom_identifer,
                                callback=rl_callback))

auth_router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/sign_up")
async def create_user(user_details:CreateUser,user_service: UserService=Depends(getSession)):
    try:
        user_exist=user_service.UserExists(user_details.email)
        if user_exist is True:
            raise HTTPException(status_code=400,detail="This email is already registered")
        user= await user_service.Create_User(user_details)
        email=user.email
        token =create_url({"email":email,"uid":user.uid},salt="verify_email")
        qr=urlencode({"token": token})
        link=f"http://{configs.Domain}/api/1.0.1/auth/verify?{qr}"
        html_message=f"""<h1>verify your email
        <p>
        <a href="{link}">link</a>
        <p>This link is valid for 15min</p>
        </h1>"""
        send_email.delay(subject="verify your email",body=html_message,recipients=[email]) # type: ignore
        return user
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@auth_router.get("/verify")
async def verify_email(token: str=Query(...), user_service: UserService = Depends(getSession)):
    token_data = decode_url(token,salt="verify_email")
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    email = token_data["email"]

    user = await user_service.getUserByEmail(email)  
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await user_service.updateUser(user, user_data={"is_verified": True}) 
    return JSONResponse(content={"message": "Email verified successfully"})

@auth_router.post("/login",dependencies=[ratelimiter])
async def Login(user_details:LoginUser,user_service: UserService=Depends(getSession)):
    password=user_details.password
    user=await user_service.getUserByEmail(user_details.email)
    if user is not None:
        isveryfied=verify_password_hash(password,user.password_hash)
        if isveryfied:

            if not user.is_verified:
                raise HTTPException(status_code=400,detail="Please verify your email")

            access_token=create_token(user_data={"email":user.email,"uid":user.uid})
            
            refresh_token=create_token(user_data={"email":user.email,"uid":user.uid},expiry=timedelta(days=2),refresh_token=True)

            return JSONResponse(content={
                "message":"Login Successfull",
                "user":user.uid,
                "email":user.email,
                "access_token":access_token,
                "refresh_token":refresh_token
            })
    raise HTTPException(status_code=400,detail="Invalid Password")

@auth_router.get("/me",dependencies=[role_che])
async def get_user(user:User=Depends(get_current_user)):
    return user

@auth_router.get("/All",dependencies=[Depends(RoleChecker(["admin"]))])
async def admin_route(user_service:UserService=Depends(getSession)):
    try:
        users=await user_service.get_All_Users()
        return users
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))  

@auth_router.post("/logout")
async def logout(token_data:dict=Depends(AccessTokenBearer())):
    token_id=token_data['jti']
    await add_to_blocklist(token_id)
    return JSONResponse(content={"message":"Logout Successfull","token_id":token_id})

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

@auth_router.get("/refresh")
async def refresh_access_token(token_data: dict = Depends(RefreshTokenBearer())):
    user = token_data["user"]

    new_access_token = create_token(
        user_data={"email": user["email"], "uid": user["uid"]},
        refresh_token=False
    )

    return JSONResponse(content={
        "message": "Refresh successful",
        "access_token": new_access_token
    })

@auth_router.post("/send_emails")
async def send_emails(email: Address):
    body="<h1>Hello From AI</h1>"
    subject="Fastapi-Mail Module"
    try:
        print("RECIPIENTS:", email.recipents)
        send_email.delay(subject=subject,body=body,recipients=email.recipents) # type: ignore
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    return {"message": "Email sent successfully"}

@auth_router.post("/password_reset_request",dependencies=[ratelimiter])
async def Password_reset_request(email: PassswordReset,user_service:UserService=Depends(getSession)):

    user=await user_service.getUserByEmail(email.email)
    if user is not None:
        try:
            token =create_url({"email":email.email},salt="reset_password")
            link=f"http://{configs.Domain}/api/1.0.1/auth/password_reset/{token}"
            html_message=f"""<h1>Reset_password
            <p>
            <a href="{link}">link</a>
            <p>This email is valid for 15min</p>
            </p>
            </h1>"""
            send_email.delay(subject="Reset Password",body=html_message,recipients=[email.email]) # type: ignore
            return JSONResponse(content={"message":"Password Reset Link Sent plzz check your email"})
        except Exception as e:
            logger.error(str(e))
        raise HTTPException(status_code=400,detail="Error in sending email")

@auth_router.post("/password_reset/{token}")
async def Password_reset_confirm(token:str,password: passwordResetConfirm,user_service:UserService=Depends(getSession)):
    newpassword=password.new_password
    confirmpassword=password.confirm_password

    token_data=decode_url(token,salt="reset_password")
    if token_data is None:
        raise HTTPException(status_code=400,detail="Invalid token")
    if token_data is None:
        raise HTTPException(status_code=400,detail="Invalid or expired token")

    if newpassword!=confirmpassword:
        raise HTTPException(status_code=400,detail="newPassword does not match confirmpassword")
    user=await user_service.getUserByEmail(token_data['email'])
    if user is None:
        raise HTTPException(status_code=400,detail="User not found")
    user.password_hash=generate_password_hash(password.new_password)
    await user_service.updateUser(user,user_data={"password_hash":user.password_hash})
    return JSONResponse(content={"message":"Password Reset Successfull"})