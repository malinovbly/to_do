# src/utils.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from uuid import uuid4

from src.models.user import UserModel
from src.schemas.schemas import NewUser, UserRole


# user
def create_user(user: NewUser, db: Session):
    try:
        check_username(user, db)

        db_user = UserModel(
            id=uuid4(),
            name=user.name,
            role=UserRole.USER,
            api_key=uuid4()
        )
        db.add(db_user)
        db.commit()
        return db_user

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def check_username(user: NewUser, db: Session):
    if len(user.name) < 5:
        raise HTTPException(status_code=400, detail="Username must be longer than 4")

    db_username = db.execute(
        select(UserModel).filter_by(name=user.name)
    ).scalar_one_or_none()

    if db_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")


# admin
def check_user_is_admin(api_key: str, db: Session):
    ...


def delete_user_by_id(user_id: str, db: Session):
    ...


# task

# other
def get_api_key(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(' ')
    if len(token) == 1:
        raise HTTPException(status_code=404, detail="Invalid Authorization")
    else:
        return token[1]
