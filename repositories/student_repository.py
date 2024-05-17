import logging
from typing import List, Optional

from pydantic import parse_obj_as
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from models import attendance, classes, meetings, students, students_classes
from schemas.class_schema import ClassWithStudents
from schemas.student_schema import StudentForClass


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


def add_student_to_class_by_id(db: Session, student_id: int, class_id: int):
    stmt = students_classes.insert().values(student_id=student_id, class_id=class_id)
    db.execute(stmt)
    db.commit()


def remove_student_from_class_by_id(db: Session, student_id: int, class_id: int):
    stmt = students_classes.delete().where(
        and_(
            students_classes.c.student_id == student_id,
            students_classes.c.class_id == class_id,
        )
    )
    db.execute(stmt)
    db.commit()
