from contextvars import Token
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError
from models import users  
from passlib.context import CryptContext
from database import get_db
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = {"user": data}
    try:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)  
        to_encode.update({"exp": expire.isoformat()})
        SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
        ALGORITHM = os.getenv("ALGORITHM", "HS256")    
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise HTTPException(status_code=500, detail="Error encoding JWT")

def serialize_datetime(user):
    try:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    except AttributeError:
        raise HTTPException(status_code=500, detail="Error serializing user data")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    try:
        user_query = select(users).where(users.c.email == email) 
        user = db.execute(user_query).first()    
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error during authentication")
