import logging
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import TokenResponse, UserCreate, UserLogin
from services.user_service import authenticate_user, create_access_token, serialize_datetime
from repositories.user_repository import get_user_by_email, insert_new_user, get_user_by_id
import os
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

@router.post("/users/", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):    
    try:
        existing_user = get_user_by_email(db, user.email)
    except Exception as e:  
        raise HTTPException(status_code=500, detail="Internal server error")
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user_id = insert_new_user(db, user.email, user.name, user.password)
    user = get_user_by_id(db, new_user_id)
    user_data = serialize_datetime(user)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    access_token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):    
    try:
        authenticated_user = authenticate_user(db, user.email, user.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_data = serialize_datetime(authenticated_user)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    access_token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
