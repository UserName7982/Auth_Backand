from fastapi import HTTPException
from redis.asyncio import Redis
from src.config import configs

redis=Redis(host=configs.URL_REDIS,port=configs.REDIS_PORT,db=0,encoding="utf-8",decode_responses=True)
Expiry=3600
async def add_to_blocklist(jti:str):
    try:
        await redis.set(name=jti,value="",ex=Expiry)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

async def check_in_blocklist(jti:str):
    try:
        return await redis.get(jti)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))