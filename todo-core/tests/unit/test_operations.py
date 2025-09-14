"""Unit tests for task operations.

Following Constitutional requirement: Test-First Development
These tests MUST fail initially (RED phase)
"""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from todo_core.models import Task, TaskStatus
from todo_core.operations import create_task, get_task, list_tasks, update_task, delete_task

def test_create_task(db_session):
    """Test task creation operation."""
    task = create_task(db_session, "Test task")

    assert isinstance(task.id, UUID)
    assert task.title == "Test task"
    assert task.status == TaskStatus.PENDING

    db_task = db_session.query(Task).filter_by(id=task.id).first()
    assert db_task is not None
    assert db_task.title == "Test task"

def test_get_task(db_session):
    """Test retrieving a task by ID."""
    task = create_task(db_session, "Test task")

    retrieved = get_task(db_session, task.id)
    assert retrieved is not None
    assert retrieved.id == task.id
    assert retrieved.title == task.title

def test_get_nonexistent_task(db_session):
    """Test that getting a nonexistent task returns None."""
    task = get_task(db_session, UUID('00000000-0000-0000-0000-000000000000'))
    assert task is None

def test_list_tasks(db_session):
    """Test listing all tasks."""
    create_task(db_session, "Task 1")
    create_task(db_session, "Task 2")
    create_task(db_session, "Task 3")

    tasks = list_tasks(db_session)
    assert len(tasks) == 3
    assert all(isinstance(t, Task) for t in tasks)
    assert {t.title for t in tasks} == {"Task 1", "Task 2", "Task 3"}

def test_list_tasks_by_status(db_session):
    """Test filtering tasks by status."""
    t1 = create_task(db_session, "Task 1")
    t2 = create_task(db_session, "Task 2")
    t3 = create_task(db_session, "Task 3")

    update_task(db_session, t1.id, status=TaskStatus.COMPLETED)
    update_task(db_session, t2.id, status=TaskStatus.COMPLETED)

    pending = list_tasks(db_session, status=TaskStatus.PENDING)
    completed = list_tasks(db_session, status=TaskStatus.COMPLETED)

    assert len(pending) == 1
    assert len(completed) == 2
    assert pending[0].title == "Task 3"
    assert {t.title for t in completed} == {"Task 1", "Task 2"}

def test_update_task(db_session):
    """Test updating a task."""
    task = create_task(db_session, "Original title")
    original_updated_at = task.updated_at

    # Wait a moment to ensure timestamp difference
    import time
    time.sleep(0.1)

    updated = update_task(
        db_session,
        task.id,
        title="New title",
        status=TaskStatus.COMPLETED
    )

    assert updated.title == "New title"
    assert updated.status == TaskStatus.COMPLETED
    assert updated.updated_at > original_updated_at

def test_update_nonexistent_task(db_session):
    """Test that updating a nonexistent task raises an error."""
    with pytest.raises(ValueError):
        update_task(
            db_session,
            UUID('00000000-0000-0000-0000-000000000000'),
            title="New title"
        )

def test_delete_task(db_session):
    """Test deleting a task."""
    task = create_task(db_session, "Test task")

    delete_task(db_session, task.id)

    assert get_task(db_session, task.id) is None
    assert db_session.query(Task).filter_by(id=task.id).first() is None

def test_delete_nonexistent_task(db_session):
    """Test that deleting a nonexistent task raises an error."""
    with pytest.raises(ValueError):
        delete_task(db_session, UUID('00000000-0000-0000-0000-000000000000'))