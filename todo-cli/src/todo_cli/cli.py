"""User-friendly CLI for todo application.

Following Constitutional requirements:
- CLI interface must be user-friendly
- Support --help, --version flags
- Use standard Unix exit codes
- Rich text output for better UX
"""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todo_core.models import Base, TaskStatus
from todo_core.operations import (
    create_task, get_task, list_tasks, update_task, delete_task
)

from . import __version__

# Create console for rich output
console = Console()

# Database setup (same as core for MVP)
engine = create_engine("sqlite:///todo.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def display_tasks(tasks, show_status: bool = True):
    """Display tasks in a rich table.

    Args:
        tasks: List of tasks to display
        show_status: Whether to show status column
    """
    table = Table(show_header=True)
    table.add_column("#", style="cyan")
    table.add_column("Title", style="white")
    if show_status:
        table.add_column("Status", style="green")

    for i, task in enumerate(tasks, 1):
        row = [str(i), task.title]
        if show_status:
            status_style = "green" if task.status == TaskStatus.COMPLETED else "yellow"
            row.append(f"[{status_style}]{task.status.value}[/{status_style}]")
        table.add_row(*row)

    console.print(table)

@click.group()
@click.version_option(version=__version__, prog_name="todo")
def cli():
    """Todo application CLI.

    A user-friendly command-line interface for managing tasks.
    """
    pass

@cli.command()
@click.argument("title")
def add(title: str):
    """Add a new task."""
    db = next(get_db())
    task = create_task(db, title)
    console.print(f"Added task: [cyan]{task.title}[/cyan]")

@cli.command()
@click.option("--all", is_flag=True, help="Show all tasks")
@click.option("--done", is_flag=True, help="Show completed tasks")
@click.option("--pending", is_flag=True, help="Show pending tasks")
def list(all: bool, done: bool, pending: bool):
    """List tasks."""
    db = next(get_db())
    status = None
    if done:
        status = TaskStatus.COMPLETED
    elif pending:
        status = TaskStatus.PENDING

    tasks = list_tasks(db, status=status)
    if not tasks:
        console.print("[yellow]No tasks found[/yellow]")
        return

    display_tasks(tasks)

@cli.command()
@click.argument("task_number", type=int)
def done(task_number: int):
    """Mark a task as completed."""
    db = next(get_db())
    tasks = list_tasks(db)
    if not 1 <= task_number <= len(tasks):
        console.print("[red]Error: Task not found[/red]", err=True)
        sys.exit(1)

    task = tasks[task_number - 1]
    updated = update_task(db, task.id, status=TaskStatus.COMPLETED)
    console.print(f"Completed task: [green]{updated.title}[/green]")

@cli.command()
@click.argument("task_number", type=int)
def rm(task_number: int):
    """Remove a task."""
    db = next(get_db())
    tasks = list_tasks(db)
    if not 1 <= task_number <= len(tasks):
        console.print("[red]Error: Task not found[/red]", err=True)
        sys.exit(1)

    task = tasks[task_number - 1]
    delete_task(db, task.id)
    console.print(f"Removed task: [red]{task.title}[/red]")

def main():
    """Entry point for the CLI."""
    cli()