from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from models import users
from services.user_service import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.execute(select(users).where(users.c.email == email)).scalar()


def insert_new_user(db: Session, email: str, name: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = users.insert().values(
        email=email, name=name, hashed_password=hashed_password
    )
    result = db.execute(db_user)
    db.commit()
    return result.inserted_primary_key[0]


def get_user_by_id(db: Session, user_id: int):
    return db.execute(select(users).where(users.c.id == user_id)).first()
