from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories.class_repository import get_class_by_id
from repositories.meeting_repository import (create_meeting_for_class,
                                             get_meeting_by_class_id_and_date,
                                             get_meeting_by_current_time,
                                             get_meeting_by_id_with_students)
from repositories.meeting_repository import get_meetings_by_class_id

import logging

from repositories.student_repository import add_new_attendance, get_students_for_class

logging.basicConfig(level=logging.DEBUG)

def get_meetings_for_class(class_id: int, teacher_id: int):
    class_ = get_class_by_id(class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")    
    if teacher_id != class_.teacher_id:
        raise HTTPException(status_code=403, detail="You don't have permission to view this class")
    result = get_meetings_by_class_id(class_id);    
    return result


def create_meeting(class_id: int):
    class_ = get_class_by_id(class_id)

    today = datetime.now().date()
    day_of_week = today.weekday()

    days_until_meeting = (class_.week_day - day_of_week) % 7
    if (
        days_until_meeting == 0
        and datetime.now().time() > datetime.strptime(class_.end_time, "%H:%M").time()
    ):
        days_until_meeting = 7

    meeting_date = today + timedelta(days=days_until_meeting)

    meeting = get_meeting_by_class_id_and_date(class_id, meeting_date)
    if not meeting:
        new_meeting_id = create_meeting_for_class(class_id, meeting_date, class_.teacher_id)
        students = get_students_for_class(class_id)
        for student in students:
            add_new_attendance(new_meeting_id, student.id)
        return {"message": "Meeting created successfully"}
    else:
        return {"message": "Meeting already exists"}


def fetch_meeting_by_current_time(db: Session, teacher_id: int):
    current_time = datetime.now()
    meeting_to_get = get_meeting_by_current_time(db, current_time)
    if not meeting_to_get:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if meeting_to_get.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this meeting"
        )
    else:
        return meeting_to_get


def fetch_meeting_by_id(meeting_id: int, teacher_id: int):
    meeting_to_get = get_meeting_by_id_with_students(meeting_id)        
    if not meeting_to_get:
        raise HTTPException(status_code=404, detail="Meeting not found")
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
