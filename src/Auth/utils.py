from datetime import datetime, timedelta, timezone
import logging
from math import ceil
from fastapi import HTTPException, Request, Response
from passlib.context import CryptContext
import uuid
import jwt
from src.config import configs
from itsdangerous import URLSafeTimedSerializer

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
Access_token_expiry=3600

def generate_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password_hash(password: str, hash: str)->bool:
    return pwd_context.verify(password, hash)

def create_token(user_data: dict,expiry: timedelta=None,refresh_token:bool=False): # type: ignore
    payload={}
    now=datetime.now(timezone.utc)
    payload['user'] = user_data
    payload['exp'] = now + (expiry if expiry else timedelta(seconds=Access_token_expiry))
    payload['jti']=str(uuid.uuid4())
    payload['iat'] = now
    payload['refresh_token'] = refresh_token
    
    token=jwt.encode(payload=payload,
                     key=configs.JWT_key,
                     algorithm=configs.Alogrithm,
                    )

    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, configs.JWT_key, algorithms=[configs.Alogrithm])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise jwt.ExpiredSignatureError("Token has expired") from e

serializer=URLSafeTimedSerializer(configs.JWT_key,salt="eamil-configuration")

def create_url(data:dict,salt:str):
    return serializer.dumps(data,salt=salt)

def decode_url(token:str,salt:str):
    try:
        token_data=serializer.loads(token,salt=salt,max_age=900)
        return token_data
    except Exception as e:
        logging.error(str(e))

from fastapi import Request
from fastapi.responses import JSONResponse

async def rl_callback(request: Request, response: Response, pexpire: int):
    retry_after = ceil(pexpire / 1000)
    raise HTTPException(
        status_code=429,
        detail={"detail": "Rate limit exceeded", "retry_after_sec": retry_after},
        headers={"Retry-After": str(retry_after)},
    )
