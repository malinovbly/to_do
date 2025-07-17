# src/utils/user.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from sqlalchemy.future import select

from src.hash_password import HashPassword
from src.models import UserModel
from src.schemas import NewUser, UserRole


def create_user_in_db(db: Session, user: NewUser):
    check_username(user, db)
    new_user_password, new_user_salt = HashPassword.hash_password(user.password)

    db_user = UserModel(
        id=uuid4(),
        name=user.name,
        role=UserRole.USER,
        password=new_user_password,
        salt=new_user_salt
    )
    db.add(db_user)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"User with such data already exists. DB error: {e.orig}")

    db.refresh(db_user)
    return db_user


def check_username(user: NewUser, db: Session):
    if len(user.name) < 5:
        raise HTTPException(status_code=400, detail="Username must be longer than 4")

    db_user = db.execute(select(UserModel).filter_by(name=user.name)).scalar_one_or_none()
    if db_user is not None:
        raise HTTPException(status_code=409, detail="Username already exists")

    return True


def get_user(db: Session, user_id: str = None, name: str = None):
    try:
        if user_id is not None:
            return db.execute(select(UserModel).filter_by(id=user_id)).scalar_one_or_none()
        elif name is not None:
            return db.execute(select(UserModel).filter_by(name=name)).scalar_one_or_none()
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")
