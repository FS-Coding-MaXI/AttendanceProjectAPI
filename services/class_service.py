from sqlalchemy.orm import Session
from repositories.class_repository import check_class_conflict, create_class, get_classes_for_teacher
from fastapi import HTTPException

def validate_and_create_class(db: Session, class_info, current_user):
    conflict = check_class_conflict(db, current_user.id, class_info.week_day, class_info.start_time, class_info.end_time)
    if conflict:
        raise HTTPException(status_code=400, detail="A class already exists in the specified timeframe")
    create_class(db, class_info.name, current_user.id, class_info.week_day, class_info.start_time, class_info.end_time)
    return class_info

def fetch_classes_for_user(db: Session, teacher_id: int):
    return get_classes_for_teacher(db, teacher_id)
