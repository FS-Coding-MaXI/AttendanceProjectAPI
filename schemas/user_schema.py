from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# User Base Schema
class UserBase(BaseModel):
    name: str
    email: EmailStr


# Schema for User Creation
class UserCreate(UserBase):
    password: str


# Schema for User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for Public User Data (without sensitive data)
class UserPublic(UserBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
