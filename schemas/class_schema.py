from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ClassCreate(BaseModel):    
    name: str
    week_day: int
    start_time: str
    end_time: str

class ClassPublic(ClassCreate): 
    id: int
    teacher_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

