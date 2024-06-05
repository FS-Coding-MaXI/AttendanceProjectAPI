import base64
import logging
import os
from sqlite3 import IntegrityError
from typing import Annotated, List
from urllib.request import Request

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models import students

from fastapi import APIRouter, Depends, File, Form, HTTPException, Header, UploadFile, status
from sqlalchemy import insert
from sqlalchemy.orm import Session

from database import get_db
from database import engine
from sqlalchemy.orm import Session, sessionmaker
from schemas.student_schema import StudentBase
from schemas.user_schema import UserPublic
from services.student_service import (
    add_student_to_class_service,
    get_students_by_search_term,
    remove_student_from_class_service,
)
from services.user_service import get_current_user
from services.ml_service import add_new_student_to_dataframe
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()


@router.get("/students/{search_term}", response_model=List[StudentBase])
async def get_students(
    search_term: str,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return get_students_by_search_term(db, search_term)


@router.post("/students/{student_id}/class/{class_id}")
async def add_student_to_class(
    student_id: int,
    class_id: int,
    current_user: UserPublic = Depends(get_current_user),
):
    return add_student_to_class_service(current_user.id, student_id, class_id)


@router.delete("/students/{student_id}/class/{class_id}")
async def remove_student_from_class(
    student_id: int,
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
):
    return remove_student_from_class_service(db, current_user.id, student_id, class_id)

class StudentCreateRequest(BaseModel):
    name: str
    email: str
    pictures: List[str]

@router.post("/students/create", status_code=201)
async def create_student(student: StudentCreateRequest):
    db = SessionLocal()
    stmt = insert(students).values(name=student.name, email=student.email)
    try:
        result = db.execute(stmt)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    student_id = result.inserted_primary_key[0]

    student_image_folder = f'images/student-{student_id}'
    os.makedirs(student_image_folder, exist_ok=True)

    for index, picture_base64 in enumerate(student.pictures):
        logging.info(f"Saving picture {index} for student {student_id}")
        picture_data = base64.b64decode(picture_base64.split(",")[1])
        picture_filename = f'picture_{index}.jpg' 
        picture_path = os.path.join(student_image_folder, picture_filename)
        with open(picture_path, "wb") as buffer:
            buffer.write(picture_data)

    add_new_student_to_dataframe(student_id)

    return JSONResponse(content={"id": student_id, "name": student.name, "email": student.email}, status_code=201)