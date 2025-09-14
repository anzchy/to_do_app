"""Unit tests for the Task model.

Following Constitutional requirement: Test-First Development
These tests MUST fail initially (RED phase)
"""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from todo_core.models import Task, TaskStatus

def test_task_creation(db_session):
    """Test that a task can be created with required fields."""
    task = Task(title="Test task")
    db_session.add(task)
    db_session.commit()

    assert isinstance(task.id, UUID)
    assert task.title == "Test task"
    assert task.status == TaskStatus.PENDING
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)

def test_task_title_required(db_session):
    """Test that task title is required."""
    with pytest.raises(ValueError):
        Task(title=None)

def test_task_title_max_length(db_session):
    """Test that task title has maximum length of 200."""
    with pytest.raises(ValueError):
        Task(title="x" * 201)

def test_task_status_must_be_valid(db_session):
    """Test that task status must be a valid TaskStatus."""
    with pytest.raises(ValueError):
        Task(title="Test", status="INVALID")

def test_task_timestamps_auto_set(db_session):
    """Test that created_at and updated_at are automatically set."""
    before = datetime.now(timezone.utc)
    task = Task(title="Test task")
    db_session.add(task)
    db_session.commit()
    after = datetime.now(timezone.utc)

    assert before <= task.created_at <= after
    assert before <= task.updated_at <= after

def test_task_update_timestamp_auto_updates(db_session):
    """Test that updated_at automatically updates."""
    task = Task(title="Test task")
    db_session.add(task)
    db_session.commit()
    original_updated_at = task.updated_at

    # Wait a moment to ensure timestamp difference
    import time
    time.sleep(0.1)

    task.title = "Updated task"
    db_session.commit()

    assert task.updated_at > original_updated_at

def test_task_status_transition(db_session):
    """Test that task status can transition between states."""
    task = Task(title="Test task")
    assert task.status == TaskStatus.PENDING

    task.status = TaskStatus.COMPLETED
    assert task.status == TaskStatus.COMPLETED

    task.status = TaskStatus.PENDING
    assert task.status == TaskStatus.PENDING