# src/api/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas.schemas import NewUser, User
from src.database.database import get_db


router = APIRouter()


@router.post(path="/register", tags=["user"], response_model=User)
def register(user: NewUser, db: Session = Depends(get_db)):
    pass
