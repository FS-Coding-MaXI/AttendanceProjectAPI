from sqlalchemy.orm import Session
from models import classes
from sqlalchemy.sql import select, insert

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
    return db.execute(class_query).scalars().all()
