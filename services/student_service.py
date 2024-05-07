from sqlalchemy import select
from models import students
from sqlalchemy.orm import Session
from repositories.student_repository import (
    get_student_by_id,
    get_students_by_email,
    get_students_by_name,
)
import logging

logging.basicConfig(level=logging.DEBUG)


def get_students_by_search_term(db: Session, search_term: str):
    if search_term == "":
        return []

    if search_term.isnumeric():
        return get_student_by_id(db, int(search_term))
    else:
        students = []
        students.append(get_students_by_name(db, search_term))
        students.append(get_students_by_email(db, search_term))
        logging.debug(students)

    return students
