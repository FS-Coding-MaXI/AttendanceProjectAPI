from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.meeting_repository import (
    get_meeting_by_current_time,
    get_meeting_by_id
)
def fetch_meeting_by_current_time(db: Session, teacher_id: int):
    current_time = datetime.now()
    meeting_to_get =  get_meeting_by_current_time(db, current_time)
    if not meeting_to_get:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if meeting_to_get.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this meeting"
        )
    else:
        return meeting_to_get
    
def fetch_meeting_by_id(db: Session, meeting_id: int, teacher_id: int):
    meeting_to_get = get_meeting_by_id(db, meeting_id)
    if not meeting_to_get:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if meeting_to_get.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this meeting"
        )
    else:
        return meeting_to_get

def fetch_students_by_meeting_id(db: Session, meeting_id: int, teacher_id: int):
    meeting_to_get = get_meeting_by_id(db, meeting_id)
    if not meeting_to_get:
        raise HTTPException(status_code=404, detail="Meeting {meeting_id} not found")
    if meeting_to_get.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this meeting"
        )
    else:
        return meeting_to_get
    
def cancel_meeting_by_id(db: Session, meeting_id: int, teacher_id: int):
    meeting_to_cancel = get_meeting_by_id(db, meeting_id)
    if not meeting_to_cancel:
        raise HTTPException(status_code=404, detail="Meeting {meeting_id} not found")
    if meeting_to_cancel.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to cancel this meeting"
        )
    else:
        return {"message": "Meeting {meeting_id} cancelled successfully"}