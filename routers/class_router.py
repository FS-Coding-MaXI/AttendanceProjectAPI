import logging
from typing import List
from urllib.request import Request
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.class_schema import ClassCreate, ClassPublic 
from schemas.user_schema import UserPublic
from services.class_service import validate_and_create_class, fetch_classes_for_user
from services.user_service import get_current_user

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

@router.post("/classes/", response_model=ClassCreate, status_code=status.HTTP_201_CREATED)
async def create_class_endpoint(newClass: ClassCreate, db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)):    
    logging.debug(f"Creating class {newClass.name} for user {current_user.id}")
    return validate_and_create_class(db, newClass, current_user)

@router.get("/classes/", response_model=List[ClassPublic])
async def get_classes_for_user_endpoint(db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)):    
    return fetch_classes_for_user(db, current_user.id)
