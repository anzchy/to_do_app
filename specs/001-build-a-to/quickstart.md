# Quickstart Guide

## Setup

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize database
```bash
alembic upgrade head
```

## Running the Application

1. Start the application
```bash
uvicorn app.main:app --reload
```

2. Access the application
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Quick Test

1. Create a new task
Using the web interface:
- Navigate to http://localhost:8000
- Click "New Task"
- Fill in the task details
- Click "Create"

Using curl:
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Get milk and eggs",
    "due_date": "2025-09-15T00:00:00Z",
    "priority": "HIGH"
  }'
```

2. List all tasks
- Web Interface: http://localhost:8000
- API: `curl http://localhost:8000/tasks`

3. Mark task as completed
- Web Interface: Click the checkbox next to the task
- API:
```bash
# Replace {task_id} with the actual ID
curl -X PUT http://localhost:8000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "COMPLETED"
  }'
```

## Development Workflow

1. Create a new branch for your feature
```bash
git checkout -b feature/your-feature-name
```

2. Run tests
```bash
pytest
```

3. Check code style
```bash
flake8
black .
```

## Common Operations

### Task Management
- Create task: POST /tasks or use web form
- List tasks: GET /tasks or visit homepage
- Update task: PUT /tasks/{id} or use web form
- Delete task: DELETE /tasks/{id} or click delete button
- Reorder tasks: Drag and drop tasks in the web interface

### Filtering and Sorting
- Filter by status: Click status tabs in web interface
- Filter by priority: Use priority dropdown
- Sort by due date: Click due date header
- Sort by priority: Click priority header

### Task States
- Priority levels: HIGH, MEDIUM, LOW
- Status values: PENDING, COMPLETED

## Template Structure
```
templates/
├── base.html              # Base template with common layout
└── tasks/
    ├── list.html         # Main task list view
    ├── create.html       # Task creation form
    └── _task.html        # Single task partial template
```

## Troubleshooting

1. Database issues
```bash
# Reset database
rm todo.db
alembic upgrade head
```

2. Template updates not showing
- Clear browser cache
- Check template inheritance
- Verify partial update targets

3. HTMX issues
- Check browser console for errors
- Verify HX-Request headers
- Check response status codes

4. API connection issues
- Verify server is running on port 8000
- Check error responses in Network tab
- Verify URL paths are correct