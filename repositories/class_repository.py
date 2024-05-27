import logging
from typing import List, Optional

from fastapi import Depends
from pydantic import parse_obj_as
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import select

from database import engine, get_db
from models import attendance, classes, meetings, students, students_classes
from schemas.class_schema import ClassWithStudents
from schemas.student_schema import StudentForClass

logging.basicConfig(level=logging.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_all_classes():
    db = SessionLocal()
    try:
        class_query = select(classes)
        result = db.execute(class_query).all()
        return result
    finally:
        db.close()


def check_class_conflict(
    db: Session, teacher_id: int, week_day: int, start_time: str, end_time: str
):
    conflict_query = select(classes).where(
        (classes.c.teacher_id == teacher_id)
        & (classes.c.week_day == week_day)
        & (
            ((classes.c.start_time <= start_time) & (classes.c.end_time > start_time))
            | ((classes.c.start_time < end_time) & (classes.c.end_time >= end_time))
        )
    )
    return db.execute(conflict_query).first()


def create_class(
    db: Session,
    name: str,
    teacher_id: int,
    week_day: int,
    start_time: str,
    end_time: str,
):
    new_class = classes.insert().values(
        name=name,
        description="",
        teacher_id=teacher_id,
        week_day=week_day,
        start_time=start_time,
        end_time=end_time,
    )
    result = db.execute(new_class)
    db.commit()
    class_id = result.inserted_primary_key[0]
    return class_id


def get_classes_for_teacher(teacher_id: int):
    db = SessionLocal()
    try:
        class_query = select(classes).where(classes.c.teacher_id == teacher_id)
        reuslt = db.execute(class_query).all()
        return reuslt
    finally:
        db.close()


def get_class_by_id(class_id: int):
    db = SessionLocal()
    try:
        class_query = select(classes).where(classes.c.id == class_id)
        result = db.execute(class_query).first()
        return result
    finally:
        db.close()


def get_class_by_id_with_students(class_id: int) -> Optional[ClassWithStudents]:
    db = SessionLocal()
    stmt = (
        select(
            classes.c.id.label("id"),
            classes.c.name.label("name"),
            classes.c.teacher_id.label("teacher_id"),
            classes.c.week_day.label("week_day"),
            classes.c.start_time.label("start_time"),
            classes.c.end_time.label("end_time"),
            classes.c.created_at.label("created_at"),
            classes.c.updated_at.label("updated_at"),
        )
        .select_from(classes)
        .outerjoin(meetings, classes.c.id == meetings.c.class_id)
        .where(classes.c.id == class_id)
        .group_by(classes.c.id)
    )

    class_result = db.execute(stmt).first()._asdict()

    number_of_meetings = (
        select(func.count(meetings.c.id).label("n_of_meetings"))
        .where(meetings.c.class_id == class_id)
        .where(meetings.c.cancelled == False)
        .group_by(meetings.c.class_id)
    )
    meetings_result = db.execute(number_of_meetings)
    if meetings_result.rowcount > 0:
        meetings_result = meetings_result.first()._asdict()
    else:
        meetings_result = {"n_of_meetings": 0}
    class_result["n_of_meetings"] = meetings_result["n_of_meetings"]

    if class_result:
        stmt_students = (
            select(
                students.c.id.label("id"),
                students.c.name.label("name"),
                students.c.email.label("email"),
            )
            .select_from(students)
            .join(students_classes, students.c.id == students_classes.c.student_id)
            .where(students_classes.c.class_id == class_id)
            .group_by(students.c.id)
        )

        students_results = db.execute(stmt_students).all()
        student_dicts = [student._asdict() for student in students_results]

        for student in student_dicts:
            stmt_attendance = (
                select(
                    func.count(attendance.c.student_id).label("present_n_times"),
                )
                .select_from(attendance)
                .outerjoin(meetings, attendance.c.meeting_id == meetings.c.id)
                .where(
                    and_(
                        meetings.c.class_id == class_id,
                        meetings.c.cancelled == False,
                        attendance.c.student_id == student["id"],
                        attendance.c.presence == True,
                    )
                )
                .group_by(attendance.c.student_id)
            )

            attendance_results = db.execute(stmt_attendance)
            if attendance_results.rowcount > 0:
                attendance_results = attendance_results.first()._asdict()
                student["present_n_times"] = attendance_results["present_n_times"]
            else:
                student["present_n_times"] = 0

        class_result["students"] = student_dicts

        return ClassWithStudents(**class_result)
    else:
        return None


def delete_class_by_id(db: Session, class_id: int):
    delete_query = classes.delete().where(classes.c.id == class_id)
    db.execute(delete_query)
    db.commit()
