# src/api/admin.py
from fastapi import APIRouter


router = APIRouter()


@router.delete(path="/user/delete", tags=["admin", "user"])
def delete_user():
    pass
