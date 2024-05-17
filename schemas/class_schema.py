from pydantic import BaseModel, EmailStr, parse_obj_as
from datetime import datetime
from typing import Optional

from schemas.student_schema import StudentForClass

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


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
