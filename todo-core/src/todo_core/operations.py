"""Task operations module.

Following Constitutional requirements:
- No Repository pattern (use SQLAlchemy directly)
- No service layer abstractions
- Real database operations (no mocking)
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from .models import Task, TaskStatus

def create_task(db: Session, title: str) -> Task:
    """Create a new task.

    Args:
        db: Database session
        title: Task title

    Returns:
        The created task
    """
    task = Task(title=title)
    db.add(task)
    db.commit()
    return task

def get_task(db: Session, task_id: UUID) -> Optional[Task]:
    """Get a task by ID.

    Args:
        db: Database session
        task_id: Task UUID

    Returns:
        Task if found, None otherwise
    """
    return db.query(Task).filter(Task.id == task_id).first()

def list_tasks(db: Session, status: Optional[TaskStatus] = None) -> List[Task]:
    """List all tasks, optionally filtered by status.

    Args:
        db: Database session
        status: Optional status filter

    Returns:
        List of tasks
    """
    query = db.query(Task)
    if status is not None:
        query = query.filter(Task.status == status)
    return query.all()

def update_task(
    db: Session,
    task_id: UUID,
    title: Optional[str] = None,
    status: Optional[TaskStatus] = None
) -> Task:
    """Update a task.

    Args:
        db: Database session
        task_id: Task UUID
        title: Optional new title
        status: Optional new status

    Returns:
        Updated task

    Raises:
        ValueError: If task not found
    """
    task = get_task(db, task_id)
    if task is None:
        raise ValueError(f"Task {task_id} not found")

    if title is not None:
        task.title = title
    if status is not None:
        task.status = status

    db.commit()
    return task

def delete_task(db: Session, task_id: UUID) -> None:
    """Delete a task.

    Args:
        db: Database session
        task_id: Task UUID

    Raises:
        ValueError: If task not found
    """
    task = get_task(db, task_id)
    if task is None:
        raise ValueError(f"Task {task_id} not found")

    db.delete(task)
    db.commit()