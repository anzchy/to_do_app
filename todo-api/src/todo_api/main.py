"""FastAPI application for todo web interface.

Following Constitutional requirements:
- Use frameworks directly (FastAPI, Jinja2)
- No unnecessary abstractions
- Simple HTMX-based interface
"""

from uuid import UUID
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from todo_core.models import Base, TaskStatus
from todo_core.operations import (
    create_task, get_task, list_tasks, update_task, delete_task
)
import uvicorn

# Create FastAPI app
app = FastAPI(title="Todo API")

# Get the directory where this file is located
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Render main task list."""
    tasks = list_tasks(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tasks": tasks}
    )

@app.post("/tasks")
async def add_task(
    request: Request,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    """Add a new task."""
    task = create_task(db, title)
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "_task.html",
            {"request": request, "task": task}
        )
    return RedirectResponse(url="/", status_code=303)

@app.put("/tasks/{task_id}")
async def toggle_task(
    request: Request,
    task_id: UUID,
    db: Session = Depends(get_db),
):
    """Toggle task completion status."""
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_status = (
        TaskStatus.COMPLETED
        if task.status == TaskStatus.PENDING
        else TaskStatus.PENDING
    )
    task = update_task(db, task_id, status=new_status)

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "_task.html",
            {"request": request, "task": task}
        )
    return RedirectResponse(url="/", status_code=303)

@app.delete("/tasks/{task_id}")
async def remove_task(
    request: Request,
    task_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a task."""
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task(db, task_id)
    if request.headers.get("HX-Request"):
        return ""
    return RedirectResponse(url="/", status_code=303)