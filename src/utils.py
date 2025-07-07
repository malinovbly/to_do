# src/utils.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from uuid import uuid4
from jose import jwt, JWTError

from src.database.database import get_db
from src.security import oauth2_scheme
from src.models.user import UserModel
from src.schemas.schemas import NewUser, UserRole, LoginData, User
from src.hash_password import HashPassword
from src.config.settings import settings


# user
def create_user(user: NewUser, db: Session) -> User:
    try:
        check_username(user, db)
        new_user_password, new_user_salt = HashPassword.hash_password(user.password)
        new_user = {
            "id": uuid4(),
            "name": user.name,
            "role": UserRole.USER,
            "password": new_user_password,
            "salt": new_user_salt
        }
        db_user = UserModel(**new_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return User(**new_user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def check_username(user: NewUser, db: Session):
    if len(user.name) < 5:
        raise HTTPException(status_code=400, detail="Username must be longer than 4")

    db_username = db.execute(
        select(UserModel).filter_by(name=user.name)
    ).scalar_one_or_none()

    if db_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")


def get_user(db: Session, user_id: str = None, name: str = None):
    if user_id is not None:
        return db.execute(select(UserModel).filter_by(id=user_id)).scalar_one_or_none()
    if name is not None:
        return db.execute(select(UserModel).filter_by(name=name)).scalar_one_or_none()


# admin
def user_is_admin(db: Session):
    ...


def delete_user(db: Session, user_id: str = None, name: str = None):
    ...


# auth
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise credentials_exception
    return User(
        id=db_user.id,
        name=db_user.name,
        role=db_user.role,
        password=db_user.password,
        salt=db_user.salt
    )


def authenticate_user(data: LoginData, db: Session) -> UserModel:
    db_user = get_user(db, name=data.name)
    if (db_user is None) or (not HashPassword.verify(db_user, data.password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user


# task
