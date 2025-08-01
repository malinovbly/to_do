# src/api/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.database import get_db
from src.security import get_current_user
from src.schemas import User, UserRole, Ok
from src.utils import delete_user_from_db, get_all_users_from_db


router = APIRouter()


@router.get(path="/admin/all-users", tags=["admin"], response_model=List[User])
def get_all_users(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.role == UserRole.ADMIN:
        return get_all_users_from_db(db)


@router.delete(path="/admin/delete-user", tags=["admin"], response_model=Ok)
def delete_user(
        user_id: str = None,
        username: str = None,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.role == UserRole.ADMIN:
        if (current_user.name == username) or (current_user.id == user_id):
            raise HTTPException(status_code=403, detail="Forbidden")
        return delete_user_from_db(db, user_id=user_id, name=username)
    raise HTTPException(status_code=403, detail="Forbidden")
