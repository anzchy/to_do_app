"""CLI interface for todo-core.

Following Constitutional requirements:
- Every library must expose CLI interface
- Support --help, --version, --format flags
- Use standard Unix exit codes
"""

from typing import Optional
import json
import sys
from uuid import UUID

import click
from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from . import __version__
from .models import Base, Task, TaskStatus
from .operations import create_task, get_task, list_tasks, update_task, delete_task

# Create console for rich output
console = Console()

# Database setup
engine = create_engine("sqlite:///todo.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def format_task(task: Task, format: str = "json") -> str:
    """Format a task for output.

    Args:
        task: Task to format
        format: Output format ("json" or "table")

    Returns:
        Formatted task string
    """
    if format == "json":
        return json.dumps({
            "id": str(task.id),
            "title": task.title,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })
    else:
        table = Table(show_header=True)
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Status")
        table.add_column("Created")
        table.add_column("Updated")

        table.add_row(
            str(task.id),
            task.title,
            task.status.value,
            task.created_at.isoformat(),
            task.updated_at.isoformat()
        )

        return table

def format_task_list(tasks: list[Task], format: str = "json") -> str:
    """Format a list of tasks for output.

    Args:
        tasks: List of tasks
        format: Output format ("json" or "table")

    Returns:
        Formatted task list string
    """
    if format == "json":
        return json.dumps([{
            "id": str(task.id),
            "title": task.title,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        } for task in tasks])
    else:
        table = Table(show_header=True)
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Status")
        table.add_column("Created")
        table.add_column("Updated")

        for task in tasks:
            table.add_row(
                str(task.id),
                task.title,
                task.status.value,
                task.created_at.isoformat(),
                task.updated_at.isoformat()
            )

        return table

@click.group()
@click.version_option(version=__version__, prog_name="todo-core")
def cli():
    """Todo core library CLI.

    Provides command-line interface for todo-core operations.
    """
    pass

@cli.command()
@click.argument("title")
@click.option("--format", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def create(title: str, format: str):
    """Create a new task."""
    db = next(get_db())
    task = create_task(db, title)
    output = format_task(task, format)

    if format == "json":
        click.echo(output)
    else:
        console.print(output)

@cli.command()
@click.option("--status", type=click.Choice(["PENDING", "COMPLETED"]),
              help="Filter by status")
@click.option("--format", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def list(status: Optional[str], format: str):
    """List all tasks."""
    db = next(get_db())
    task_status = TaskStatus(status) if status else None
    tasks = list_tasks(db, status=task_status)
    output = format_task_list(tasks, format)

    if format == "json":
        click.echo(output)
    else:
        console.print(output)

@cli.command()
@click.argument("task_id")
@click.option("--title", help="New task title")
@click.option("--status", type=click.Choice(["PENDING", "COMPLETED"]),
              help="New task status")
@click.option("--format", type=click.Choice(["json", "table"]), default="json",
              help="Output format")
def update(task_id: str, title: Optional[str], status: Optional[str],
          format: str):
    """Update a task."""
    try:
        db = next(get_db())
        task_status = TaskStatus(status) if status else None
        task = update_task(db, UUID(task_id), title=title, status=task_status)
        output = format_task(task, format)

        if format == "json":
            click.echo(output)
        else:
            console.print(output)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument("task_id")
def delete(task_id: str):
    """Delete a task."""
    try:
        db = next(get_db())
        delete_task(db, UUID(task_id))
        click.echo("Task deleted")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli()