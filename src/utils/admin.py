# src/utils/admin.py
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.schemas import Ok
from src.utils.user import get_user


def delete_user_from_db(db: Session, user_id: str = None, name: str = None):
    db_user = get_user(db, user_id, name)
    if db_user is not None:
        db.delete(db_user)
        db.commit()
        return Ok
    else:
        raise HTTPException(status_code=404, detail="User not found")
