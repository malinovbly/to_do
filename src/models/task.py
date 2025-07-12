# src/models/task.py
from sqlalchemy import Column, String, ForeignKey, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.schemas.schemas import TaskImportance
from src.database.database import Base


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(UUID(as_uuid=True), unique=True, index=True, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    importance = Column(SqlEnum(TaskImportance), default=TaskImportance.LOW)
    is_completed = Column(Boolean, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)

    user = relationship("UserModel", back_populates="tasks")

    def __repr__(self):
        return f"<TaskModel(id={self.id}, name={self.name}, user_id={self.user_id})>"
