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

logging.basicConfig(level=logging.DEBUG)

def check_class_conflict(db: Session, teacher_id: int, week_day: int, start_time: str, end_time: str):
    conflict_query = select(classes).where(
        (classes.c.teacher_id == teacher_id) &
        (classes.c.week_day == week_day) &
        (
            ((classes.c.start_time <= start_time) & (classes.c.end_time > start_time)) |
            ((classes.c.start_time < end_time) & (classes.c.end_time >= end_time))
        )
    )
    return db.execute(conflict_query).first()

def create_class(db: Session, name: str, teacher_id: int, week_day: int, start_time: str, end_time: str):
    new_class = classes.insert().values(
        name=name,
        description="",
        teacher_id=teacher_id,
        week_day=week_day,
        start_time=start_time,
        end_time=end_time
    )
    db.execute(new_class)
    db.commit()

def get_classes_for_teacher(db: Session, teacher_id: int):
    class_query = select(classes).where(classes.c.teacher_id == teacher_id)    
    return db.execute(class_query).all()

def get_class_by_id(db: Session, class_id: int):
    class_query = select(classes).where(classes.c.id == class_id)
    return db.execute(class_query).first()
    
def get_class_by_id_with_students(db: Session, class_id: int) -> Optional[ClassWithStudents]:
    stmt = select(
        classes.c.id.label("id"),
        classes.c.name.label("name"),
        classes.c.teacher_id.label("teacher_id"),
        classes.c.week_day.label("week_day"),
        classes.c.start_time.label("start_time"),
        classes.c.end_time.label("end_time"),
        classes.c.created_at.label("created_at"),
        classes.c.updated_at.label("updated_at"),
        func.count(meetings.c.id).label("n_of_meetings")
    ).select_from(classes)\
        .outerjoin(meetings, classes.c.id == meetings.c.class_id)\
        .where(classes.c.id == class_id)\
        .group_by(classes.c.id)

    class_result = db.execute(stmt).first()._asdict()  
    
    if class_result:
        stmt_students = select(
            students.c.id.label("id"),
            students.c.name.label("name"),
            students.c.email.label("email"),            
        ).select_from(students).join(students_classes, students.c.id == students_classes.c.student_id)\
            .where(students_classes.c.class_id == class_id).group_by(students.c.id)            

        students_results = db.execute(stmt_students).all()
        student_dicts = [student._asdict() for student in students_results]          

        for student in student_dicts:                      
            stmt_attendance = select(
                func.count(attendance.c.student_id).label("present_n_times"),
            ).select_from(attendance).outerjoin(meetings, attendance.c.meeting_id == meetings.c.id)\
                .where(and_(meetings.c.class_id == class_id, attendance.c.student_id == student['id']))\
                .group_by(attendance.c.student_id)
                        
            attendance_results = db.execute(stmt_attendance)                   
            if attendance_results.rowcount > 0:
                attendance_results = attendance_results.first()._asdict()
                student['present_n_times'] = attendance_results['present_n_times']
            else:
                student['present_n_times'] = 0

        class_result['students'] = student_dicts        
        
        return ClassWithStudents(**class_result)
    else:
        return None

def delete_class_by_id(db: Session, class_id: int):
    delete_query = classes.delete().where(classes.c.id == class_id)
    db.execute(delete_query)
    db.commit()