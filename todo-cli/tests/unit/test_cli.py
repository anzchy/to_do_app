"""Unit tests for user-friendly CLI interface.

Following Constitutional requirement: Test-First Development
These tests MUST fail initially (RED phase)
"""

from click.testing import CliRunner
import pytest
from rich.console import Console

from todo_cli.cli import cli

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

def test_cli_version(runner):
    """Test --version flag shows version."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "todo version" in result.output

def test_cli_help(runner):
    """Test --help flag shows help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output

def test_add_task(runner):
    """Test adding a task."""
    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Added task:" in result.output
    assert "Buy milk" in result.output

def test_add_task_without_title(runner):
    """Test that adding task without title fails."""
    result = runner.invoke(cli, ["add"])
    assert result.exit_code == 2
    assert "Error: Missing argument" in result.output

def test_list_tasks(runner):
    """Test listing tasks."""
    # Add some test tasks
    runner.invoke(cli, ["add", "Task 1"])
    runner.invoke(cli, ["add", "Task 2"])
    runner.invoke(cli, ["add", "Task 3"])

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" in result.output
    assert "Task 3" in result.output

def test_list_tasks_by_status(runner):
    """Test listing tasks filtered by status."""
    # Add tasks and complete some
    runner.invoke(cli, ["add", "Task 1"])
    runner.invoke(cli, ["add", "Task 2"])
    runner.invoke(cli, ["done", "1"])  # Complete first task

    # List pending tasks
    result = runner.invoke(cli, ["list", "--pending"])
    assert result.exit_code == 0
    assert "Task 2" in result.output
    assert "Task 1" not in result.output

    # List completed tasks
    result = runner.invoke(cli, ["list", "--done"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" not in result.output

def test_done_task(runner):
    """Test marking a task as done."""
    runner.invoke(cli, ["add", "Test task"])
    result = runner.invoke(cli, ["done", "1"])
    assert result.exit_code == 0
    assert "Completed task:" in result.output
    assert "Test task" in result.output

def test_done_nonexistent_task(runner):
    """Test marking nonexistent task as done."""
    result = runner.invoke(cli, ["done", "999"])
    assert result.exit_code == 1
    assert "Error: Task not found" in result.output

def test_remove_task(runner):
    """Test removing a task."""
    runner.invoke(cli, ["add", "Test task"])
    result = runner.invoke(cli, ["rm", "1"])
    assert result.exit_code == 0
    assert "Removed task:" in result.output
    assert "Test task" in result.output

def test_remove_nonexistent_task(runner):
    """Test removing nonexistent task."""
    result = runner.invoke(cli, ["rm", "999"])
    assert result.exit_code == 1
    assert "Error: Task not found" in result.output

def test_output_style(runner):
    """Test rich text output styling."""
    console = Console()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    # Rich styling should be present (table borders, colors)
    assert "─" in result.output  # Table border
    assert "pending" in result.output.lower()
    assert "completed" in result.output.lower()