# src/api/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.security import api_key_header
from src.utils import get_api_key, check_user_is_admin, delete_user_by_id


router = APIRouter()


@router.delete(path="/user/delete", tags=["admin", "user"])
def delete_user(
        user_id: str,
        authorization: str = Depends(api_key_header),
        db: Session = Depends(get_db)
):
    api_key = get_api_key(authorization)
    if check_user_is_admin(api_key, db):
        return delete_user_by_id(user_id, db)
