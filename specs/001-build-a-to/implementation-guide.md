# Implementation Guide

This document provides detailed implementation sequences and references to help developers follow the task-driven implementation approach.

## Implementation Sequence

### Phase 1: Foundation Setup
**Reference**: [data-model.md](data-model.md) for entity definitions

1. **Database Models** (`src/models/task.py`)
   - Implement Task model based on data-model.md fields
   - Add PriorityLevel and TaskStatus enums
   - Reference: data-model.md lines 6-15 for field specifications

2. **Database Setup** (`alembic/versions/`)
   - Create migration for Task table
   - Reference: data-model.md validation rules for constraints

3. **Service Layer** (`src/services/task_service.py`)
   - Implement CRUD operations
   - Add reordering logic for display_order
   - Reference: contracts/openapi.yaml for expected operations

### Phase 2: API Implementation
**Reference**: [contracts/openapi.yaml](contracts/openapi.yaml) for endpoint specifications

4. **API Routes** (`src/api/tasks.py`)
   - Implement each endpoint from openapi.yaml
   - Return both JSON (for API) and HTML (for HTMX)
   - Reference specific paths and schemas in openapi.yaml

5. **Request/Response Models** (`src/schemas/`)
   - Create Pydantic models matching openapi.yaml schemas
   - Reference: openapi.yaml components/schemas section

### Phase 3: Template Implementation
**Reference**: [research.md](research.md) HTMX best practices section

6. **Base Template** (`src/templates/base.html`)
   - Include HTMX, TailwindCSS, Sortable.js
   - Set up common layout structure

7. **Task Templates** (`src/templates/tasks/`)
   - list.html: Main task list with sorting/filtering
   - _task.html: Individual task component with HTMX attributes
   - create.html: Task creation form
   - Reference: quickstart.md template structure

### Phase 4: Frontend Integration
8. **HTMX Routes** (mixed into `src/api/tasks.py`)
   - Add template rendering to existing routes
   - Implement partial updates for task modifications
   - Reference: research.md HTMX best practices

9. **Static Assets** (`src/static/`)
   - Custom CSS for drag-and-drop styling
   - JavaScript for Sortable.js integration

### Phase 5: Testing
**Reference**: [research.md](research.md) testing strategy section

10. **Contract Tests** (`tests/contract/`)
    - Test each API endpoint against openapi.yaml
    - Reference: contracts/openapi.yaml for expected responses

11. **Integration Tests** (`tests/integration/`)
    - Test user scenarios from spec.md
    - Reference: spec.md acceptance scenarios

12. **E2E Tests** (`tests/e2e/`)
    - Test complete user workflows
    - Reference: spec.md user stories

## Code Implementation Patterns

### SQLAlchemy Model Pattern
```python
# Reference: data-model.md Task entity
class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)  # From data-model.md validation
    # ... other fields from data-model.md
```

### FastAPI Route Pattern
```python
# Reference: openapi.yaml /tasks endpoint
@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = None,  # From openapi.yaml parameters
    priority: Optional[PriorityLevel] = None,
    sort_by: Optional[str] = None,
    request: Request = None
):
    # Return JSON for API calls, HTML for browser requests
    if request.headers.get("HX-Request"):
        # Return partial HTML for HTMX
        pass
    elif request.headers.get("Accept") == "application/json":
        # Return JSON for API
        pass
    else:
        # Return full HTML page
        pass
```

### HTMX Template Pattern
```html
<!-- Reference: research.md HTMX best practices -->
<div id="task-list" hx-get="/tasks" hx-trigger="load">
    {% for task in tasks %}
    <div class="task-item"
         hx-put="/tasks/{{ task.id }}"
         hx-swap="outerHTML"
         data-task-id="{{ task.id }}">
        <!-- Task content from data-model.md fields -->
    </div>
    {% endfor %}
</div>
```

## Cross-Reference Map

| Implementation Step | Primary Reference | Secondary References |
|-------------------|------------------|-------------------|
| Task Model | data-model.md lines 6-15 | research.md SQLAlchemy practices |
| API Endpoints | openapi.yaml paths section | spec.md functional requirements |
| Templates | quickstart.md template structure | research.md HTMX practices |
| User Flows | spec.md acceptance scenarios | quickstart.md common operations |
| Testing | research.md testing strategy | spec.md edge cases |

## File Dependencies

### Creation Order (to avoid circular dependencies):
1. `src/models/task.py` → No dependencies
2. `src/schemas/task.py` → Depends on models
3. `src/services/task_service.py` → Depends on models
4. `src/api/tasks.py` → Depends on services, schemas
5. Templates → Depend on API routes being defined
6. Tests → Depend on all above components

### Critical References During Implementation:
- **Models**: Always reference data-model.md field specifications
- **APIs**: Always validate against openapi.yaml contracts
- **Templates**: Follow structure in quickstart.md, patterns in research.md
- **Tests**: Implement scenarios from spec.md acceptance criteria