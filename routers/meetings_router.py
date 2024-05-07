from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from schemas.student_schema import StudentBase
from schemas.user_schema import UserPublic
from services.user_service import get_current_user
from services.meeting_service import (
    fetch_meeting_by_current_time, 
    fetch_meeting_by_id,
    fetch_students_by_meeting_id,
    cancel_meeting_by_id
)

router = APIRouter()

@router.get("/meetings/")
async def get_meeting_by_current_time(
    db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)
):
    return fetch_meeting_by_current_time(db, current_user.id)

@router.get("/meetings/{meeting_id}")
async def get_meeting_by_id(
    meeting_id: int, db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)
):
    return fetch_meeting_by_id(db, meeting_id, current_user.id)

@router.get("/meetings/{meeting_id}/students", response_model=List[StudentBase])
async def get_studets_by_meeting_id(
     meeting_id: int, db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)
):
    return fetch_students_by_meeting_id(db, meeting_id, current_user.id)

@router.post("/meetings/{meeting_id}/cancel")
async def cancel_meeting(
    meeting_id: int, db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)
):
    return cancel_meeting_by_id(db, meeting_id, current_user.id)