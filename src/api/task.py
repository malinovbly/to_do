# src/api/task.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.models.user import UserModel
from src.schemas.schemas import NewTask, Task, Ok
from src.database.database import get_db
from src.security import get_current_user
from src.utils import create_task_in_db, get_task_from_db, delete_task_from_db


router = APIRouter()


@router.post(path="/tasks", tags=["task"], response_model=Task)
def create_task(
        task: NewTask = Depends(),
        current_user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return create_task_in_db(db, current_user, task)


@router.get(path="/tasks", tags=["task"], response_model=List[Task])
def get_all_tasks(
        current_user: UserModel = Depends(get_current_user)
):
    return list(current_user.tasks)


@router.get(path="/tasks/{task_id}", tags=["task"], response_model=Task)
def get_task(
        task_id: UUID,
        current_user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return get_task_from_db(db, current_user, task_id)


@router.put(path="/tasks/{task_id}", tags=["task"], response_model=Task)
def change_task():
    pass


@router.post(path="/tasks/{task_id}", tags=["task"], response_model=Ok)
def complete_task():
    pass


@router.delete(path="/tasks/{task_id}", tags=["task"], response_model=Ok)
def delete_task(
        task_id: UUID,
        current_user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return delete_task_from_db(db, current_user, task_id)
