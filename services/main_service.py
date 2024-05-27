from sqlalchemy import and_, func, select, update
from sqlalchemy.orm import Session, sessionmaker
from models import meetings, students, students_classes, classes, attendance, users

from database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import logging

logging.basicConfig(level=logging.DEBUG)

async def get_meetings():
    db = SessionLocal()
    try:
        meeting_query = select(meetings)
        result = db.execute(meeting_query).all()
        logging.debug(result)
        return [meeting._asdict() for meeting in result]
    finally:
        db.close()

async def get_students(): 
    db = SessionLocal()
    try:
        student_query = select(students)
        result = db.execute(student_query).all()
        logging.debug(result)
        return [student._asdict() for student in result]
    finally:
        db.close()

async def get_classes():
    db = SessionLocal()
    try:
        class_query = select(classes)
        result = db.execute(class_query).all()
        logging.debug(result)
        return [class_._asdict() for class_ in result]
    finally:
        db.close()

async def get_attendance():
    db = SessionLocal()
    try:
        attendance_query = select(attendance)
        result = db.execute(attendance_query).all()
        logging.debug(result)
        return [attendance._asdict() for attendance in result]
    finally:
        db.close()

async def get_students_classes():
    db = SessionLocal()
    try:
        students_classes_query = select(students_classes)
        result = db.execute(students_classes_query).all()
        logging.debug(result)
        return [students_class._asdict() for students_class in result]
    finally:
        db.close()

async def get_users():
    db = SessionLocal()
    try:
        users_query = select(users)
        result = db.execute(users_query).all()
        logging.debug(result)
        return [user._asdict() for user in result]
    finally:
        db.close()

