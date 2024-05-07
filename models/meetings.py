from sqlalchemy import Column, Integer, String, Table, ForeignKey, Date, DateTime
from sqlalchemy.sql import func
from database import metadata

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
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)

# Create meeings router, service, repository
# route add function to get current meeting (by time) - get
# route cancel meeting - post
# get meeting by id and get students by meeting id
