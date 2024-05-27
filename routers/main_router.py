from fastapi import APIRouter
from services.main_service import get_attendance, get_classes, get_meetings, get_students, get_students_classes, get_users

import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

@router.get("/main")
async def get_all_data():
    meetings = await get_meetings()
    students = await get_students()
    classes = await get_classes()
    attendance = await get_attendance()
    students_classes = await get_students_classes()
    users = await get_users()
    return {
        "meetings": meetings,
        "students": students,
        "classes": classes,
        "attendance": attendance,
        "students_classes": students_classes,
        "users": users
    }        