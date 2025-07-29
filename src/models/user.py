# src/models/user.py
from sqlalchemy import Column, String, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.database.database import Base
from src.schemas import UserRole


class UserModel(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False, unique=True)
    role = Column(SqlEnum(UserRole), default=UserRole.USER)

    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    tasks = relationship("TaskModel", back_populates="user", passive_deletes=True)
