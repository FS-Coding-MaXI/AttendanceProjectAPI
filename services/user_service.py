from contextvars import Token
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError
from models import users  
from passlib.context import CryptContext
from database import get_db
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
import logging

from schemas.user_schema import UserPublic

logging.basicConfig(level=logging.DEBUG)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = {"user": data}
    try:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)  
        to_encode.update({"exp": expire.timestamp()})
        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")    
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logging.debug(f"Encoded JWT: {encoded_jwt}")
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

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserPublic:
    credentials_exception = HTTPException(      
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("token")    
    if not token:
        raise HTTPException(status_code=401, detail="No authentication token found")    
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])        
        user = payload.get("user")
        user_id = user.get("id")
    except JWTError as e:
        raise credentials_exception
    user_query = select(users).where(users.c.id == user_id)
    user = db.execute(user_query).first()
    if user is None:
        raise credentials_exception
    return user
