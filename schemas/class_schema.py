from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, parse_obj_as

from schemas.student_schema import StudentForClass


class ClassCreate(BaseModel):
    name: str
    week_day: int
    start_time: str
    end_time: str


class ClassPublic(ClassCreate):
    id: int
    teacher_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ClassWithStudents(ClassPublic):
    n_of_meetings: int
    students: Optional[List[StudentForClass]] = []
