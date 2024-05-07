from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import metadata

classes = Table(
    "classes",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("description", String),
    Column("teacher_id", Integer, ForeignKey("users.id")),
    Column("week_day", Integer),
    Column("start_time", String),
    Column("end_time", String),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)
