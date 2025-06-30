# src/api/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.security import security


router = APIRouter()


@router.delete(path="/user/delete", tags=["admin", "user"])
def delete_user(
        user_id: str,
        authorization: str = Depends(security),
        db: Session = Depends(get_db)
):
    ...
