from sqlmodel import SQLModel
from src.DB import Models
from src.config import configs
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker

engine=create_async_engine(configs.DATABASE_URL)

AsyncSessionLocal=async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session




