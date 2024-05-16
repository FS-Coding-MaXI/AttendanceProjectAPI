import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from models import classes, meetings, attendance, students, students_classes
from sqlalchemy.sql import select
from schemas.class_schema import ClassWithStudents
from schemas.student_schema import StudentForClass
from sqlalchemy import or_, select, func, and_
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

def get_students_by_name_or_email(db: Session, searchTerm: str):
    stmt = select(students).where( or_(students.c.email.ilike(f"%{searchTerm}%"), students.c.name.ilike(f"%{searchTerm}%")))
    result =  db.execute(stmt).all()
    return [row._asdict() for row in result]


def get_student_by_id(db: Session, student_id: int):
    stmt = select(students).where(students.c.id == student_id)
    return db.execute(stmt).first()._asdict()

def add_student_to_class_by_id(db: Session, student_id: int, class_id: int):
    stmt = students_classes.insert().values(student_id=student_id, class_id=class_id)
    db.execute(stmt)
    db.commit()

def remove_student_from_class_by_id(db: Session, student_id: int, class_id: int):
    stmt = students_classes.delete().where(and_(students_classes.c.student_id == student_id, students_classes.c.class_id == class_id))
    db.execute(stmt)
    db.commit()