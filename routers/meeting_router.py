from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.meeting_schema import MeetingWithStudents
from schemas.student_schema import StudentForMeeting
from schemas.user_schema import UserPublic
from services.meeting_service import (cancel_meeting_by_id,
                                      fetch_meeting_by_current_time,
                                      fetch_meeting_by_id)
from services.user_service import get_current_user

router = APIRouter()


@router.get("/meetings/")
async def get_meeting_by_current_time(
    db: Session = Depends(get_db), current_user: UserPublic = Depends(get_current_user)
):
    return fetch_meeting_by_current_time(db, current_user.id)


@router.get("/meetings/{meeting_id}", response_model=MeetingWithStudents)
async def get_meeting_by_id(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return fetch_meeting_by_id(db, meeting_id, current_user.id)


@router.post("/meetings/{meeting_id}/cancel")
async def cancel_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return cancel_meeting_by_id(db, meeting_id, current_user.id)
