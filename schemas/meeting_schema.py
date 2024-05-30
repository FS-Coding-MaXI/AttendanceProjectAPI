from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.student_schema import StudentForMeeting


class MeetingCreate(BaseModel):
    teacher_id: int
    class_id: int
    start_date: datetime
    end_date: datetime


class MeetingPublic(MeetingCreate):
    id: int
    cancelled: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MeetingWithStudents(MeetingPublic):
    students: Optional[List[StudentForMeeting]] = []
