# src/database/init_data.py
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from uuid import uuid4

from src.models.user import UserModel
from src.schemas.schemas import UserRole
from src.config.settings import settings
from src.hash_password import HashPassword


def create_admin(db: Session):
    db_admin = db.execute(
        select(UserModel).filter_by(name="admin")
    ).scalar_one_or_none()

    if db_admin is None:
        hashed = HashPassword.hash_password(settings.ADMIN_PASSWORD)
        new_admin = UserModel(
            id=uuid4(),
            name="admin",
            role=UserRole.ADMIN,
            password=hashed[0],
            salt=hashed[1]
        )
        db.add(new_admin)
        db.commit()
        print("Admin created")
    else:
        print("Admin already exists")
