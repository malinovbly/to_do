# src/utils.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from uuid import uuid4

from src.models.user import UserModel
from src.schemas.schemas import NewUser, UserRole, User, Ok
from src.hash_password import HashPassword


# user
def create_user(user: NewUser, db: Session) -> User:
    try:
        check_username(user, db)
        new_user_password, new_user_salt = HashPassword.hash_password(user.password)
        new_user = {
            "id": uuid4(),
            "name": user.name,
            "role": UserRole.USER,
            "password": new_user_password,
            "salt": new_user_salt
        }
        db_user = UserModel(**new_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return User(**new_user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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


# admin
def delete_user_from_db(db: Session, user_id: str = None, name: str = None):
    db_user = get_user(db, user_id, name)
    if db_user is not None:
        db.delete(db_user)
        db.commit()
        return Ok
    else:
        raise HTTPException(status_code=404, detail="User not found")


# task
