"""Unit tests for FastAPI application.

Following Constitutional requirement: Test-First Development
These tests MUST fail initially (RED phase)
"""

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from todo_api.main import app, get_db
from todo_core.models import Base

# Setup in-memory database for testing
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

def test_read_main(client):
    """Test main page loads."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo App" in response.text
    assert "What needs to be done?" in response.text

def test_create_task(client):
    """Test task creation."""
    response = client.post(
        "/tasks",
        data={"title": "Test task"},
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 200
    assert "Test task" in response.text
    assert 'hx-put="/tasks/' in response.text

def test_create_task_without_title(client):
    """Test task creation without title fails."""
    response = client.post("/tasks", data={})
    assert response.status_code == 422

def test_toggle_task(client):
    """Test task completion toggle."""
    # Create a task first
    response = client.post(
        "/tasks",
        data={"title": "Test task"},
        headers={"HX-Request": "true"}
    )
    task_id = response.text.split('task-')[1].split('"')[0]

    # Toggle it
    response = client.put(
        f"/tasks/{task_id}",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 200
    assert "text-green-500" in response.text  # Completed checkmark

    # Toggle back
    response = client.put(
        f"/tasks/{task_id}",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 200
    assert "text-gray-400" in response.text  # Uncompleted circle

def test_toggle_nonexistent_task(client):
    """Test toggling nonexistent task fails."""
    response = client.put(
        "/tasks/00000000-0000-0000-0000-000000000000",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 404

def test_delete_task(client):
    """Test task deletion."""
    # Create a task first
    response = client.post(
        "/tasks",
        data={"title": "Test task"},
        headers={"HX-Request": "true"}
    )
    task_id = response.text.split('task-')[1].split('"')[0]

    # Delete it
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 200
    assert response.text == ""  # HTMX removes element

def test_delete_nonexistent_task(client):
    """Test deleting nonexistent task fails."""
    response = client.delete(
        "/tasks/00000000-0000-0000-0000-000000000000",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 404