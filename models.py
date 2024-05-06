from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean, Date, DateTime
from sqlalchemy.sql import func
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
)

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
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
)

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, unique=True, index=True),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
)

students_classes = Table(
    "students_classes",
    metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("class_id", Integer, ForeignKey("classes.id"), primary_key=True),
)

meetings = Table(
    "meetings",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("teacher_id", Integer, ForeignKey("users.id")),
    Column("class_id", Integer, ForeignKey("classes.id")),
    Column("start_time", String),
    Column("end_time", String),
    Column("date", Date),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
)

# Create meeings router, service, repository
# route add function to get current meeting (by time) - get
# route cancel meeting - post 
# get meeting by id and get students by meeting id

attendance = Table(
    "attendance",
    metadata,
    Column("meeting_id", Integer, ForeignKey("meetings.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("arrival_time", DateTime),
    Column("presence", Boolean),
    Column("was_late", Boolean),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
)
