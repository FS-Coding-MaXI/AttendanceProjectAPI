from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories.class_repository import get_class_by_id
from repositories.meeting_repository import (
    cancel_meeting,
    create_meeting_for_class,
    get_current_meeting,
    get_meeting_by_class_id_and_date,
    get_meeting_by_id,
    get_meeting_by_id_with_students,
)
from repositories.meeting_repository import get_meetings_by_class_id

import logging

from repositories.student_repository import add_new_attendance, get_students_for_class

logging.basicConfig(level=logging.DEBUG)


def get_meetings_for_class(class_id: int, teacher_id: int):
    class_ = get_class_by_id(class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    if teacher_id != class_.teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this class"
        )
    result = get_meetings_by_class_id(class_id)
    return result


from datetime import datetime, timedelta


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

    start_time = datetime.strptime(class_.start_time, "%H:%M").time()
    end_time = datetime.strptime(class_.end_time, "%H:%M").time()
    meeting_date = today + timedelta(days=days_until_meeting)

    meeting_start_datetime = datetime.combine(meeting_date, start_time)
    meeting_end_datetime = datetime.combine(meeting_date, end_time)

    meeting = get_meeting_by_class_id_and_date(class_id, meeting_start_datetime)
    if not meeting:
        new_meeting_id = create_meeting_for_class(
            class_id, meeting_start_datetime, meeting_end_datetime, class_.teacher_id
        )
        students = get_students_for_class(class_id)
        for student in students:
            add_new_attendance(new_meeting_id, student.id)
        return {"message": "Meeting created successfully"}
    else:
        return {"message": "Meeting already exists"}


def fetch_meeting_by_current_time(teacher_id: int):    
    meeting_to_get = get_current_meeting(teacher_id)
    if not meeting_to_get:
        raise HTTPException(status_code=404, detail="Meeting not found")    
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


def cancel_meeting_by_id(meeting_id: int, teacher_id: int):
    meeting_to_cancel = get_meeting_by_id(meeting_id)
    if not meeting_to_cancel:
        raise HTTPException(status_code=404, detail="Meeting {meeting_id} not found")
    if meeting_to_cancel.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to cancel this meeting"
        )
    cancel_meeting(meeting_id)
    return {"message": "Meeting cancelled successfully"}
