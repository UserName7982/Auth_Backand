from typing import List, Optional
from sqlmodel import ForeignKey, SQLModel, Field, Relationship
from sqlalchemy import Column
import sqlalchemy.dialects.mysql as mysql
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore

    uid: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )

    name: str
    email: str

    role: str = Field(
        sa_column=Column(mysql.VARCHAR(20), default="user")
    )

    password_hash: str = Field(exclude=True)

    is_verified: bool = Field(
        sa_column=Column(mysql.BOOLEAN, default=False)
    )

    created_at: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, default=datetime.utcnow)
    )

    updated_at: datetime = Field(
        sa_column=Column(
            mysql.TIMESTAMP,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
        )
    )

    is_active: bool = Field(
        sa_column=Column(mysql.BOOLEAN, default=True)
    )
