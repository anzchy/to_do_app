"""Core data models for the todo application.

Following Constitutional requirements:
- Single data model (Task)
- No DTOs unless serialization differs
- No Repository pattern or Unit of Work
- Using SQLAlchemy directly without wrappers
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class TaskStatus(str, Enum):
    """Task completion status."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class Base(DeclarativeBase):
    """Base class for all models."""
    pass

class Task(Base):
    """Task model representing a todo item.

    Constitutional compliance:
    - Single responsibility: Represents one todo item
    - No complex relationships or inheritance
    - Essential fields only (YAGNI principle)
    """
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, title: str, status: Optional[TaskStatus] = None) -> None:
        """Create a new task.

        Args:
            title: Task title (required, max 200 chars)
            status: Task status (optional, defaults to PENDING)

        Raises:
            ValueError: If title is None or exceeds 200 chars
        """
        if not title:
            raise ValueError("Task title is required")
        if len(title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        super().__init__(
            title=title,
            status=status or TaskStatus.PENDING
        )