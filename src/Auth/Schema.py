from typing import List
from pydantic import BaseModel

class User(BaseModel):
    uid: str
    name: str
    email: str
    role: str 
    is_verified: bool
    created_at: str
    updated_at: str
    is_active: bool

class CreateUser(BaseModel):
    name: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class Address(BaseModel):
    recipents: List[str]

class PassswordReset(BaseModel):
    email: str

class passwordResetConfirm(BaseModel):
    new_password: str
    confirm_password:str