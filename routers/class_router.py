import logging
from typing import List
from urllib.request import Request
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.class_schema import ClassCreate, ClassPublic, ClassWithStudents
from schemas.user_schema import UserPublic
from services.class_service import (
    fetch_class_by_id,
    remove_class,
    validate_and_create_class,
    fetch_classes_for_user,
)
from services.user_service import get_current_user

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post(
    "/classes/", response_model=ClassCreate, status_code=status.HTTP_201_CREATED
)
async def create_class_endpoint(
    newClass: ClassCreate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return validate_and_create_class(db, newClass, current_user)


@router.get("/classes/", response_model=List[ClassPublic])
async def get_classes_for_user_endpoint(
    db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)
):
    return fetch_classes_for_user(db, current_user.id)


@router.get("/classes/{class_id}/", response_model=ClassWithStudents)
async def get_class_by_id_endpoint(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return fetch_class_by_id(db, class_id, current_user.id)


@router.delete("/classes/{class_id}/")
async def delete_class_endpoint(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return remove_class(db, class_id, current_user.id)
