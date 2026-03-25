from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.comments import Comment
    from app.models.users import User

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    complete = "complete"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus), default=TaskStatus.pending, nullable=False
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(TaskPriority), default=TaskPriority.low, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    owner: Mapped[Optional["User"]] = relationship(back_populates="tasks")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )
