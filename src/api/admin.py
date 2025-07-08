# src/api/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.schemas.schemas import User, UserRole, Ok
from src.utils import delete_user_from_db
from src.security import get_current_user


router = APIRouter()


@router.delete(path="/user/delete", tags=["admin", "user"], response_model=Ok)
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
