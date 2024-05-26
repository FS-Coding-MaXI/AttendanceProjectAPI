from datetime import datetime
import logging
from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, sessionmaker

from database import engine
from models import attendance, classes, meetings, students, students_classes
from schemas.meeting_schema import MeetingWithStudents

logging.basicConfig(level=logging.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_meetings_by_class_id(class_id: int):
    db = SessionLocal()
    try:        
        meeting_query = select(meetings).where(meetings.c.class_id == class_id)        
        result = db.execute(meeting_query).all()   
        logging.debug(result)     
        return [meeting._asdict() for meeting in result]
    finally:
        db.close()


def get_next_meeting(class_id: int):
    db = SessionLocal()
    current_date = datetime.now().date()
    meeting_query = (
        select(meetings)
        .where(and_(meetings.c.class_id == class_id, meetings.c.date > current_date))
        .order_by(meetings.c.date.asc())
    )
    return db.execute(meeting_query).first()


def get_meeting_by_class_id_and_date(class_id: int, date: datetime):
    db = SessionLocal()
    try:
        meeting_query = select(meetings).where(
            and_(meetings.c.class_id == class_id, meetings.c.date == date)
        )
        result = db.execute(meeting_query).first()
        return result
    finally:
        db.close()


def create_meeting_for_class(class_id: int, date: datetime, teacher_id: int):
    db = SessionLocal()
    try:
        new_meeting = meetings.insert().values(
            class_id=class_id, date=date, teacher_id=teacher_id
        )
        result = db.execute(new_meeting)
        db.commit()
        return result.inserted_primary_key[0]
    finally:
        db.close()


def get_meeting_by_current_time(db: Session, current_time: datetime):
    meeting_query = (
        select(meetings)
        .join(classes, classes.c.id == meetings.c.class_id)
        .where(
            and_(
                classes.start_time <= current_time.strftime("%H:%M"),
                classes.end_time >= current_time.strftime("%H:%M"),
                classes.date == current_time.date(),
            )
        )
    )
    return db.execute(meeting_query).first()


def get_meeting_by_id_with_students(
    meeting_id: int
) -> Optional[MeetingWithStudents]:
    db = SessionLocal()

    stmt = (
        select(meetings)        
        .where(meetings.c.id == meeting_id)
    )

    meeting_result = db.execute(stmt).first()._asdict()
    if meeting_result:        

        class_id = meeting_result["class_id"]

        stmt_students = (
            select(students)
            .join(students_classes, students.c.id == students_classes.c.student_id)
            .where(students_classes.c.class_id == class_id)
        )

        students_results = db.execute(stmt_students).all()
        student_dicts = [student._asdict() for student in students_results]

        for student in student_dicts:
            stmt_attendance = (
                select(attendance)
                .where(
                    and_(
                        attendance.c.meeting_id == meeting_id,
                        attendance.c.student_id == student["id"],
                    )
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


def cancel_meeting_by_id(db: Session, meeting_id: int):
    meeting_query = select(meetings).where(meetings.c.id == meeting_id)
    meeting_to_cancel = db.execute(meeting_query).first()
    meeting_to_cancel["cancelled"] = True
    delete_attendance_by_meeting_id(db, meeting_id)


def delete_attendance_by_meeting_id(db: Session, meeting_id: int):
    db.execute(attendance.delete().where(attendance.c.meeting_id == meeting_id))
    db.commit()
