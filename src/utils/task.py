# src/utils/task.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from uuid import uuid4, UUID

from src.models import TaskModel
from src.schemas import User, Ok, NewTask


def create_task_in_db(db: Session, user: User, new_task: NewTask):
    if new_task.description is None:
        new_task.description = ""
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
