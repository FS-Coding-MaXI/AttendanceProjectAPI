from sqlalchemy import Column, Integer, String, Table, Boolean, Date, DateTime
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, index=True),
    Column("hashed_password", String),
    Column("created_at", DateTime),
)

classes = Table(
  "classes",
  metadata,
  Column("id", Integer, primary_key=True, index=True),
  Column("name", String, index=True),
  Column("description", String),
  Column("teacher_id", Integer),
  Column("week_day", Integer),
  Column("start_time", String),
  Column("end_time", String),
  Column("created_at", DateTime),
  Column("updated_at", DateTime)
)

students = Table(
  "students",
  metadata,
  Column("id", Integer, primary_key=True, index=True),
  Column("name", String, index=True),
  Column("email", String, index=True),  
  Column("created_at", DateTime),
  Column("updated_at", DateTime)
)

students_classes = Table(
  "students_classes",
  metadata,
  Column("student_id", Integer, primary_key=True),
  Column("class_id", Integer, primary_key=True),
)

meetings = Table(
  "meetings",
  metadata,
  Column("id", Integer, primary_key=True, index=True),
  Column("teacher_id", Integer),
  Column("class_id", Integer),  
  Column("start_time", String),
  Column("end_time", String),
  Column("date", Date),
)

attendance = Table(
  "attendance",
  metadata,  
  Column("meeting_id", Integer, primary_key=True),
  Column("student_id", Integer, primary_key=True),
  Column("arrival_time", DateTime),
  Column("presence", Boolean),
  Column("was_late", Boolean),
)