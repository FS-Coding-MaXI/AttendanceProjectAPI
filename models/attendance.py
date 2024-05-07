from sqlalchemy import Column, Integer, Table, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from database import metadata

attendance = Table(
    "attendance",
    metadata,
    Column("meeting_id", Integer, ForeignKey("meetings.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("arrival_time", DateTime),
    Column("presence", Boolean),
    Column("was_late", Boolean),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)
