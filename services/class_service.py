from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.class_repository import (
    check_class_conflict,
    create_class,
    delete_class_by_id,
    get_class_by_id,
    get_class_by_id_with_students,
    get_classes_for_teacher,
)


def validate_and_create_class(db: Session, class_info, current_user):
    conflict = check_class_conflict(
        db,
        current_user.id,
        class_info.week_day,
        class_info.start_time,
        class_info.end_time,
    )
    if conflict:
        raise HTTPException(
            status_code=400, detail="A class already exists in the specified timeframe"
        )
    new_class = create_class(
        db,
        class_info.name,
        current_user.id,
        class_info.week_day,
        class_info.start_time,
        class_info.end_time,
    )
    return new_class


def fetch_classes_for_user(teacher_id: int):
    return get_classes_for_teacher(teacher_id)


def remove_class(db: Session, class_id: int, current_user_id: int):
    class_to_delete = get_class_by_id(class_id)
    if not class_to_delete:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_to_delete.teacher_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this class"
        )

    delete_class_by_id(db, class_id)
    return {"message": "Class successfully deleted"}


def fetch_class_by_id(class_id: int, current_user_id: int):
    class_info = get_class_by_id_with_students(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_info.teacher_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this class"
        )
    return class_info
