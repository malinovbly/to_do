# src/utils.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from uuid import uuid4, UUID

from src.models.task import TaskModel
from src.models.user import UserModel
from src.schemas.schemas import NewUser, UserRole, User, Ok, NewTask
from src.hash_password import HashPassword


# user
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
def create_task_in_db(db: Session, user: User, new_task: NewTask):
    db_task = TaskModel(
        id=uuid4(),
        name=new_task.name,
        description=new_task.description,
        importance=new_task.importance,
        user_id=user.id
    )
    db.add(db_task)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Could not create task due to a database integrity error. Check if related data exists. DB error: {e.orig}"
        )

    db.refresh(db_task)
    return db_task


def get_task_from_db(db: Session, user: User, task_id: UUID):
    db_task = db.execute(select(TaskModel).filter_by(id=task_id)).scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db_task


def delete_task_from_db(db: Session, user: User, task_id: UUID):
    try:
        db_task = get_task_from_db(db, user, task_id)
        db.delete(db_task)
        db.commit()
        return Ok

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")
