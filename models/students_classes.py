from sqlalchemy import (
    Column,
    Integer,
    Table,
    ForeignKey,
)
from sqlalchemy.sql import func
from database import metadata

students_classes = Table(
    "students_classes",
    metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("class_id", Integer, ForeignKey("classes.id"), primary_key=True),
)
