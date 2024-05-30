from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StudentBase(BaseModel):
    id: int
    name: str
    email: str


class StudentForClass(BaseModel):
    id: int
    name: str
    email: str
    present_n_times: int


class Attendance(BaseModel):
    arrival_time: Optional[datetime] = None
    presence: bool
    was_late: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    meeting_id: int
    student_id: int


class StudentForMeeting(StudentBase):
    attendance: Attendance
