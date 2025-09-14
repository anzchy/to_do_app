"""Unit tests for CLI interface.

Following Constitutional requirement: Test-First Development
These tests MUST fail initially (RED phase)
"""

from click.testing import CliRunner
import json
import pytest
from uuid import UUID

from todo_core.cli import cli
from todo_core.models import TaskStatus

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

def test_cli_version(runner):
    """Test --version flag shows version."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "todo-core version" in result.output

def test_cli_help(runner):
    """Test --help flag shows help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output

def test_create_task(runner, db_session):
    """Test task creation via CLI."""
    result = runner.invoke(cli, ["create", "Test task"])
    assert result.exit_code == 0

    data = json.loads(result.output)
    assert data["title"] == "Test task"
    assert data["status"] == "PENDING"
    assert UUID(data["id"])  # Validates UUID format

def test_create_task_without_title(runner):
    """Test that creating task without title fails."""
    result = runner.invoke(cli, ["create"])
    assert result.exit_code == 2
    assert "Error: Missing argument" in result.output

def test_list_tasks(runner, db_session):
    """Test listing tasks via CLI."""
    # Create some test tasks
    runner.invoke(cli, ["create", "Task 1"])
    runner.invoke(cli, ["create", "Task 2"])
    runner.invoke(cli, ["create", "Task 3"])

    # List all tasks
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0

    data = json.loads(result.output)
    assert len(data) == 3
    assert {t["title"] for t in data} == {"Task 1", "Task 2", "Task 3"}

def test_list_tasks_by_status(runner, db_session):
    """Test listing tasks filtered by status."""
    # Create tasks and complete some
    result1 = runner.invoke(cli, ["create", "Task 1"])
    result2 = runner.invoke(cli, ["create", "Task 2"])

    task1_id = json.loads(result1.output)["id"]
    runner.invoke(cli, ["update", task1_id, "--status", "COMPLETED"])

    # List pending tasks
    result = runner.invoke(cli, ["list", "--status", "PENDING"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 1
    assert data[0]["title"] == "Task 2"

    # List completed tasks
    result = runner.invoke(cli, ["list", "--status", "COMPLETED"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"

def test_update_task(runner, db_session):
    """Test updating task via CLI."""
    # Create a task
    create_result = runner.invoke(cli, ["create", "Original title"])
    task_id = json.loads(create_result.output)["id"]

    # Update title
    result = runner.invoke(cli, ["update", task_id, "--title", "New title"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["title"] == "New title"

    # Update status
    result = runner.invoke(cli, ["update", task_id, "--status", "COMPLETED"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["status"] == "COMPLETED"

def test_update_nonexistent_task(runner):
    """Test that updating nonexistent task fails."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    result = runner.invoke(cli, ["update", fake_id, "--title", "New title"])
    assert result.exit_code == 1
    assert "Error: Task not found" in result.output

def test_delete_task(runner, db_session):
    """Test deleting task via CLI."""
    # Create a task
    create_result = runner.invoke(cli, ["create", "Test task"])
    task_id = json.loads(create_result.output)["id"]

    # Delete it
    result = runner.invoke(cli, ["delete", task_id])
    assert result.exit_code == 0
    assert "Task deleted" in result.output

    # Verify it's gone
    result = runner.invoke(cli, ["list"])
    data = json.loads(result.output)
    assert len(data) == 0

def test_delete_nonexistent_task(runner):
    """Test that deleting nonexistent task fails."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    result = runner.invoke(cli, ["delete", fake_id])
    assert result.exit_code == 1
    assert "Error: Task not found" in result.output

def test_output_format_json(runner, db_session):
    """Test JSON output format."""
    result = runner.invoke(cli, ["create", "Test task", "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, dict)
    assert "id" in data
    assert "title" in data
    assert "status" in data

def test_output_format_table(runner, db_session):
    """Test table output format."""
    result = runner.invoke(cli, ["list", "--format", "table"])
    assert result.exit_code == 0
    assert "ID" in result.output
    assert "Title" in result.output
    assert "Status" in result.output
    assert "─" in result.output  # Table border