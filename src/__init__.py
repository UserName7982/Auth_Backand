from fastapi import FastAPI
from src.Auth.routes import auth_router
from src.logger import logger
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
from src.DB.Redis import redis
from src.middleware import add_process_time_header
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.Retrival.api.route import retrieval
from src.DataIngestion.api.route import ingestion
from fastapi.middleware.cors import CORSMiddleware

version="1.0.1"
@asynccontextmanager
async def lifespan(app: FastAPI):
    await FastAPILimiter.init(redis)
    yield

app=FastAPI(version=version,description="AI Assistant",lifespan=lifespan,
    docs_url=f"/{version}/docs",
    redoc_url=f"/{version}/redoc")
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.include_router(auth_router,prefix=f"/api/{version}",tags=["auth"])
app.include_router(retrieval,prefix=f"/api/{version}",tags=["retrieval"])
app.include_router(ingestion,prefix=f"/api/{version}",tags=["ingestion"])
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1"
    ]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)