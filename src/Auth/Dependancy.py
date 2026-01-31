from typing import List
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.Auth.Services import UserService, getSession
from src.Auth.utils import verify_token
from src.DB.Redis import check_in_blocklist
class TokenBearer(HTTPBearer):
    def __init__(self,auto_error:bool=True):
        super().__init__(auto_error=auto_error)
    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        crediential=await super().__call__(request)
        if crediential is None:
            raise HTTPException(status_code=401,detail="Invalid token or token been Revoked")
        token =crediential.credentials # type: ignore
        token_data=self.decode_token(token)
        token_id=token_data['jti']
        in_blocklist=await check_in_blocklist(token_id)
        if token_data and not in_blocklist:
            self.verify_token_data(token_data)
            return token_data
        else:
            raise HTTPException(status_code=401,detail="Invalid token or token been Revoked")
    
    def decode_token(self,token):
        try:
            is_verified=verify_token(token)
            return is_verified
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))
    def verify_token_data(self,token_data:dict)->None:
        raise NotImplementedError("sub class must implement this method")
    
class AccessTokenBearer(TokenBearer):

    def verify_token_data(self ,token_data:dict)->None:
        if token_data and token_data['refresh_token']  :
            raise HTTPException(status_code=401,detail="please provide Access token")

class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self ,token_data:dict)->None:
        if token_data and not token_data['refresh_token']:
            raise HTTPException(status_code=401,detail="please provide refresh token")

async def get_current_user(token_data: dict=Depends(AccessTokenBearer()),user_service:UserService=Depends(getSession)):
        user=await user_service.getUserByEmail(token_data['user']['email'])
        if user is None:
            raise HTTPException(status_code=400,detail="User not found")
        return user

class RoleChecker():
    def __init__(self, role: List[str]):
        self.role=role
    def __call__(self,user=Depends(get_current_user))->None:
        role=user.role
        if role not in self.role:
            raise HTTPException(status_code=401,detail="You are not authorized to perform this action")
        
async def custom_identifer(request:Request):
    ip=request.client.host if request.client else "unknown"
    try:
        body=await request.json()
        email=body['email']
        return f"{ip}:{email}"
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    