from datetime import datetime
import logging
from typing import Optional

from sqlalchemy import and_, func, select, update
from sqlalchemy.orm import Session, sessionmaker

from database import engine
from models import attendance, classes, meetings, students, students_classes
from schemas.meeting_schema import MeetingWithStudents

logging.basicConfig(level=logging.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_current_meeting(teacher_id: int):
    db = SessionLocal()
    try:                
        meeting_query = (
            select(meetings)
            .where(meetings.c.teacher_id == teacher_id
            )
            .where(meetings.c.start_date <= func.now())
            .where(meetings.c.end_date >= func.now())
        )
        result = db.execute(meeting_query).first()
        logging.debug(result)
        if result:
            return result._asdict()  
        else:
            return None
    finally:
        db.close()


def get_meetings_by_class_id(class_id: int):
    db = SessionLocal()
    try:
        meeting_query = select(meetings).where(meetings.c.class_id == class_id)
        result = db.execute(meeting_query).all()        
        return [meeting._asdict() for meeting in result]
    finally:
        db.close()


def get_next_meeting(class_id: int):
    db = SessionLocal()
    current_date = datetime.now().date()
    meeting_query = (
        select(meetings)
        .where(
            and_(meetings.c.class_id == class_id, meetings.c.start_date > current_date)
        )
        .order_by(meetings.c.start_date.asc())
    )
    return db.execute(meeting_query).first()


def get_meeting_by_class_id_and_date(class_id: int, start_date: datetime):
    db = SessionLocal()
    try:
        meeting_query = select(meetings).where(
            and_(meetings.c.class_id == class_id, meetings.c.start_date == start_date)
        )
        result = db.execute(meeting_query).first()
        return result
    finally:
        db.close()


def get_meeting_by_id(meeting_id: int):
    db = SessionLocal()
    try:
        meeting_query = select(meetings).where(meetings.c.id == meeting_id)
        result = db.execute(meeting_query).first()
        return result
    finally:
        db.close()


def create_meeting_for_class(
    class_id: int, start_date: datetime, end_date: datetime, teacher_id: int
):
    db = SessionLocal()
    try:
        new_meeting = meetings.insert().values(
            class_id=class_id,
            start_date=start_date,
            end_date=end_date,
            teacher_id=teacher_id,
        )
        result = db.execute(new_meeting)
        db.commit()
        return result.inserted_primary_key[0]
    finally:
        db.close()


def get_meeting_by_id_with_students(meeting_id: int) -> Optional[MeetingWithStudents]:
    db = SessionLocal()

    stmt = select(meetings).where(meetings.c.id == meeting_id)

    meeting_result = db.execute(stmt).first()._asdict()
    if meeting_result:
        stmt_students = (
            select(students)
            .join(attendance, students.c.id == attendance.c.student_id)
            .where(attendance.c.meeting_id == meeting_id)
        )

        students_results = db.execute(stmt_students).all()
        student_dicts = [student._asdict() for student in students_results]

        for student in student_dicts:
            stmt_attendance = select(attendance).where(
                and_(
                    attendance.c.meeting_id == meeting_id,
                    attendance.c.student_id == student["id"],
                )
            )

            attendance_results = db.execute(stmt_attendance).first()._asdict()
            if attendance_results:
                student["attendance"] = attendance_results
            else:
                student["attendance"] = dict()

        meeting_result["students"] = student_dicts
        return MeetingWithStudents(**meeting_result)
    else:
        return None


def cancel_meeting(meeting_id: int):
    db = SessionLocal()
    try:
        meeting_query = (
            update(meetings).where(meetings.c.id == meeting_id).values(cancelled=True)
        )
        db.execute(meeting_query)
        db.commit()
    finally:
        db.close()


def delete_attendance_by_meeting_id(db: Session, meeting_id: int):
    db.execute(attendance.delete().where(attendance.c.meeting_id == meeting_id))
    db.commit()
