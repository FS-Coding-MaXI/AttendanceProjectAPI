import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import students
from repositories.class_repository import get_class_by_id
from repositories.meeting_repository import get_next_meeting
from repositories.student_repository import (
    add_new_attendance,
    add_student_to_class_by_id,
    get_student_by_id,
    get_students_by_name_or_email,
    remove_student_from_class_by_id,
)

logging.basicConfig(level=logging.DEBUG)


def get_students_by_search_term(db: Session, search_term: str):
    if search_term == "":
        return []

    if search_term.isnumeric():
        return [get_student_by_id(db, int(search_term))]
    else:
        return get_students_by_name_or_email(db, search_term)


def add_student_to_class_service(current_user_id: int, student_id: int, class_id: int):
    class_ = get_class_by_id(class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_.teacher_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to modify this class"
        )

    add_student_to_class_by_id(student_id, class_id)

    next_meeting = get_next_meeting(class_id)
    if next_meeting:
        add_new_attendance(student_id, next_meeting.id)

    return {"message": "Student successfully added to class"}


def remove_student_from_class_service(
    db: Session, current_user_id: int, student_id: int, class_id: int
):
    class_ = get_class_by_id(class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_.teacher_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to modify this class"
        )

    remove_student_from_class_by_id(student_id, class_id)

    return {"message": "Student successfully removed from class"}

