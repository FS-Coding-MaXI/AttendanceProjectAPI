from datetime import datetime
from sqlalchemy.orm import Session
from models import meetings
from sqlalchemy import and_, select
from models import students, students_classes


def get_meeting_by_current_time(db: Session, current_time: datetime):
    meeting_query = select(meetings).where(
        and_(
            meetings.c.start_time <= current_time.strftime("%H:%M"),
            meetings.c.end_time >= current_time.strftime("%H:%M"),
            meetings.c.date == current_time.date()
        )
    )
    return db.execute(meeting_query).first()

def get_meeting_by_id(db: Session, meeting_id: int):
    meeting_query = select(meetings).where(meetings.c.id == meeting_id)
    return db.execute(meeting_query).first()

def get_students_by_meeting_id(db: Session, meeting_id: int):
    query = (
        select(students)
        .join(students_classes, students_classes.c.student_id == students.c.id)
        .join(meetings, meetings.c.class_id == students_classes.c.class_id)
        .filter(meetings.c.id == meeting_id)
    )
    return db.execute(query).fetchall()

def cancel_meeting_by_id(db: Session, meeting_id: int):
    meeting_query = select(meetings).where(meetings.c.id == meeting_id)
    meeting_to_cancel = db.execute(meeting_query).first()
    db.execute(meetings.delete().where(meetings.c.id == meeting_id))
    db.commit()
    return meeting_to_cancel