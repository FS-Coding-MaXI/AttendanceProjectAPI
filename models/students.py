from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    DateTime,
)
from sqlalchemy.sql import func
from database import metadata

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, unique=True, index=True),
    Column("created_at", DateTime, default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)
