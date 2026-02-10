from fastapi import FastAPI
from src.Auth.routes import auth_router
from src.logger import logger
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
from src.DB.Redis import redis
from src.middleware import add_process_time_header
from starlette.middleware.base import BaseHTTPMiddleware
version="1.0.1"
@asynccontextmanager
async def lifespan(app: FastAPI):
    await FastAPILimiter.init(redis)
    yield

app=FastAPI(version=version,description="AI Assistant",lifespan=lifespan)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.include_router(auth_router,prefix=f"/api/{version}",tags=["auth"])
