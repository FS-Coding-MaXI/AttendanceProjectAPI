import logging
from typing import List, Optional

from pydantic import parse_obj_as
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy.orm import Session, sessionmaker

from database import engine

from models import attendance, classes, meetings, students, students_classes
from schemas.class_schema import ClassWithStudents
from schemas.student_schema import StudentForClass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_students_by_name_or_email(db: Session, searchTerm: str):
    stmt = select(students).where(
        or_(
            students.c.email.ilike(f"%{searchTerm}%"),
            students.c.name.ilike(f"%{searchTerm}%"),
        )
    )
    result = db.execute(stmt).all()
    return [row._asdict() for row in result]


def get_student_by_id(db: Session, student_id: int):
    stmt = select(students).where(students.c.id == student_id)
    return db.execute(stmt).first()._asdict()


def get_students_for_class(class_id: int):
    db = SessionLocal()
    try:
        stmt = (
            select(students)
            .select_from(students.join(students_classes).join(classes))
            .where(classes.c.id == class_id)
        )
        result = db.execute(stmt).all()
        return [row._asdict() for row in result]
    finally:
        db.close()


def add_new_attendance(student_id: int, meeting_id: int):
    db = SessionLocal()
    try:
        stmt = attendance.insert().values(student_id=student_id, meeting_id=meeting_id)
        db.execute(stmt)
        db.commit()
    finally:
        db.close()


def add_student_to_class_by_id(student_id: int, class_id: int):
    db = SessionLocal()
    stmt = students_classes.insert().values(student_id=student_id, class_id=class_id)
    try:
        db.execute(stmt)
        db.commit()
    finally:
        db.close()


def remove_student_from_class_by_id(student_id: int, class_id: int):
    db = SessionLocal()

    stmt = students_classes.delete().where(
        and_(
            students_classes.c.student_id == student_id,
            students_classes.c.class_id == class_id,
        )
    )
    db.execute(stmt)
    db.commit()
