import logging
from typing import List
from urllib.request import Request

from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.student_schema import StudentBase
from schemas.user_schema import UserPublic
from services.student_service import (add_student_to_class_service,
                                      get_students_by_search_term,
                                      remove_student_from_class_service)
from services.user_service import get_current_user

router = APIRouter()


@router.get("/students/{search_term}", response_model=List[StudentBase])
async def get_students(
    search_term: str,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return get_students_by_search_term(db, search_term)


@router.post("/students/{student_id}/class/{class_id}")
async def add_student_to_class(
    student_id: int,
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return add_student_to_class_service(db, current_user.id, student_id, class_id)


@router.delete("/students/{student_id}/class/{class_id}")
async def remove_student_from_class(
    student_id: int,
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return remove_student_from_class_service(db, current_user.id, student_id, class_id)
