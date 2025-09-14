# Library Specifications (Constitutional)

Following constitutional requirement: "EVERY feature as library"

## Library 1: todo-core

**Purpose**: Core business logic and data model
**No direct app code** - pure library

### Structure
```
todo-core/
├── src/
│   ├── models.py      # Task SQLAlchemy model
│   └── operations.py  # CRUD operations
├── tests/
│   ├── test_models.py
│   └── test_operations.py
├── cli.py             # Constitutional requirement
└── setup.py
```

### CLI Interface (Constitutional Requirement)
```bash
todo-core --help
todo-core list --format=json
todo-core list --format=table
todo-core create "Task title"
todo-core update <id> --title="New title" --status=COMPLETED
todo-core delete <id>
todo-core --version
```

### API
```python
from todo_core import Task, create_task, list_tasks, update_task, delete_task

# All operations return Task objects or raise exceptions
task = create_task("Buy milk")
tasks = list_tasks()
update_task(task.id, status=TaskStatus.COMPLETED)
delete_task(task.id)
```

## Library 2: todo-cli

**Purpose**: Command-line user interface
**Uses**: todo-core library

### Structure
```
todo-cli/
├── src/
│   └── cli.py         # User-friendly CLI
├── tests/
│   └── test_cli.py
├── cli.py             # Constitutional requirement
└── setup.py
```

### CLI Interface (Constitutional Requirement)
```bash
todo-cli --help
todo-cli add "Buy milk"
todo-cli list
todo-cli done <id>
todo-cli rm <id>
todo-cli --version
todo-cli --format=json  # For scripting
```

### Implementation
- Uses click or argparse
- Calls todo-core operations
- Human-readable output by default
- JSON output for scripting

## Library 3: todo-api

**Purpose**: Web interface with HTMX
**Uses**: todo-core library

### Structure
```
todo-api/
├── src/
│   ├── main.py        # FastAPI application
│   └── templates/
│       ├── list.html  # Simple task list
│       └── form.html  # Add/edit form
├── tests/
│   ├── test_api.py
│   └── test_templates.py
├── cli.py             # Constitutional requirement
└── setup.py
```

### CLI Interface (Constitutional Requirement)
```bash
todo-api --help
todo-api serve --port=8000 --host=0.0.0.0
todo-api serve --dev  # Development mode
todo-api --version
```

### Web Interface
- GET / → list.html (shows all tasks)
- GET /add → form.html (add task form)
- GET /edit/<id> → form.html (edit task form)
- POST /tasks → create task (HTMX)
- PUT /tasks/<id> → update task (HTMX)
- DELETE /tasks/<id> → delete task (HTMX)

## Constitutional Compliance

### ✅ Architecture Requirements Met
- **3 libraries** (within max 3 limit)
- **Each feature as library** (no direct app code)
- **CLI per library** (--help, --version, --format)
- **Clear purpose** for each library

### ✅ Simplicity Requirements Met
- **Using frameworks directly** (FastAPI, SQLAlchemy, click)
- **Single data model** (Task only)
- **No unnecessary patterns** (no Repository, no Service layer)

### ✅ Testing Requirements Met
- **TDD approach** (tests written first)
- **Real dependencies** (actual SQLite)
- **Contract tests** for todo-api
- **Integration tests** between libraries

## Library Dependencies
```
todo-core: SQLAlchemy, click
todo-cli: todo-core, click
todo-api: todo-core, FastAPI, Jinja2
```

## Installation & Usage
```bash
# Install libraries
pip install ./todo-core
pip install ./todo-cli
pip install ./todo-api

# Use via CLI
todo-cli add "Buy milk"
todo-api serve --port=8000

# Use as libraries
from todo_core import create_task
task = create_task("Learn Python")
```

This approach follows constitutional principles while avoiding over-engineering.