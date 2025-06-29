# src/api/task.py
from fastapi import APIRouter


router = APIRouter()


@router.post(path="/tasks", tags=["task"])
def create_task():
    pass


@router.get(path="/tasks", tags=["task"])
def get_all_tasks():
    pass


@router.put(path="/tasks/{task_id}", tags=["task"])
def change_task():
    pass


@router.post(path="/tasks/{task_id}", tags=["task"])
def complete_task():
    pass


@router.delete(path="/tasks/{task_id}", tags=["task"])
def cancel_task():
    pass
