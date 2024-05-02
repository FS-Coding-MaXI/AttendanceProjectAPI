from contextvars import Token
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError
from models import users  
from passlib.context import CryptContext
from database import get_db
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from schemas.user_schema import TokenResponse, UserCreate, UserLogin, UserPublic
from services.user_service import authenticate_user, create_access_token, get_password_hash, serialize_datetime
import os


router = APIRouter()

@router.post("/users/", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):    
    try:
        existing_user = db.execute(select(users).where(users.c.email == user.email)).scalar()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        db_user = users.insert().values(email=user.email, name=user.name, hashed_password=hashed_password)
        result = db.execute(db_user)
        db.commit()
        new_user_id = result.inserted_primary_key[0]
        user = db.execute(select(users).where(users.c.id == new_user_id)).first()
        user_data = serialize_datetime(user)
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
        access_token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error during user creation")

@router.post("/login/", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        authenticated_user = authenticate_user(db, user.email, user.password)
        if not authenticated_user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        user_data = serialize_datetime(authenticated_user)
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
        access_token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error during login")
