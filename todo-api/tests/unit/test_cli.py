"""Unit tests for API CLI interface.

Following Constitutional requirement: Test-First Development
These tests MUST fail initially (RED phase)
"""

from click.testing import CliRunner
import pytest

from todo_api.cli import cli

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

def test_cli_version(runner):
    """Test --version flag shows version."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "todo-api version" in result.output

def test_cli_help(runner):
    """Test --help flag shows help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Commands:" in result.output

def test_serve_command_help(runner):
    """Test serve command help."""
    result = runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0
    assert "Start the API server" in result.output
    assert "--host" in result.output
    assert "--port" in result.output
    assert "--reload" in result.output