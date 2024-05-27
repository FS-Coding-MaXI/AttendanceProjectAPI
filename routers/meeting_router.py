from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.meeting_schema import MeetingPublic, MeetingWithStudents
from schemas.student_schema import StudentForMeeting
from schemas.user_schema import UserPublic
from services.meeting_service import (
    cancel_meeting_by_id,
    fetch_meeting_by_current_time,
    fetch_meeting_by_id,
    get_meetings_for_class,
)
from services.user_service import get_current_user

import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.get("/meetings/{meeting_id}", response_model=MeetingWithStudents)
async def get_meeting_by_id(
    meeting_id: int,
    current_user: UserPublic = Depends(get_current_user),
):
    return fetch_meeting_by_id(meeting_id, current_user.id)

@router.get("/meetings/class/{class_id}", response_model=List[MeetingPublic])
async def get_meeting(
    class_id: int,
    current_user: UserPublic = Depends(get_current_user),
):
    return get_meetings_for_class(class_id, current_user.id)


@router.put("/meetings/{meeting_id}/cancel")
async def cancel_meeting(
    meeting_id: int,
    current_user: UserPublic = Depends(get_current_user),
):
    return cancel_meeting_by_id(meeting_id, current_user.id)

@router.get("/meetings", response_model=MeetingPublic)
async def get_current_meeting(current_user: UserPublic = Depends(get_current_user)):    
    return fetch_meeting_by_current_time(current_user.id)