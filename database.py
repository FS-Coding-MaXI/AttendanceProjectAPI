from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@db/attendanceproject"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database = Database(DATABASE_URL)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
