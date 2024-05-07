from fastapi import APIRouter, Header
import logging
from typing import List
from urllib.request import Request
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.student_schema import StudentBase
from schemas.user_schema import UserPublic
from services.student_service import get_students_by_search_term
from services.user_service import get_current_user

router = APIRouter()


@router.get("/students/{search_term}", response_model=List[StudentBase])
async def get_students(
    search_term: str,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return get_students_by_search_term(db, search_term)
