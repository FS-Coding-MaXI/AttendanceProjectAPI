from pydantic import BaseModel, EmailStr, DateTime
from typing import Optional

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
    created_at: Optional[DateTime]

    class Config:
        orm_mode = True
