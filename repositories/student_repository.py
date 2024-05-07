import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from models import classes, meetings, attendance, students, students_classes
from sqlalchemy.sql import select
from schemas.class_schema import ClassWithStudents
from schemas.student_schema import StudentForClass
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from pydantic import parse_obj_as


def get_students_by_name(db: Session, search_term: str):
    stmt = select(students).where(students.c.name.ilike(f"%{search_term}%"))
    result = db.execute(stmt).all()
    return [row._asdict() for row in result]


def get_students_by_email(db: Session, email: str):
    stmt = select(students).where(students.c.email.ilike(f"%{email}%"))
    result = db.execute(stmt).all()
    return [row._asdict() for row in result]


def get_student_by_id(db: Session, student_id: int):
    stmt = select(students).where(students.c.id == student_id)
    return db.execute(stmt).first()._asdict()
