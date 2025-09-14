"""CLI interface for todo-api.

Following Constitutional requirement:
Every library must expose CLI interface
"""

import click
import uvicorn

from . import __version__

@click.group()
@click.version_option(version=__version__, prog_name="todo-api")
def cli():
    """Todo API server CLI.

    Provides web interface for todo application.
    """
    pass

@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host: str, port: int, reload: bool):
    """Start the API server."""
    uvicorn.run(
        "todo_api.main:app",
        host=host,
        port=port,
        reload=reload
    )

def main():
    """Entry point for the CLI."""
    cli()