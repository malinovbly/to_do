# src/api/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db


router = APIRouter()


@router.delete(path="/user/delete", tags=["admin", "user"])
def delete_user(
        user_id: str,
        db: Session = Depends(get_db)
):
    ...
