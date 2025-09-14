# Simplified Data Model (Constitutional)

## Task Entity (Only)

Following constitutional principle: "Single data model? (no DTOs unless serialization differs)"

### Fields
- id: UUID (primary key)
- title: String (required, max 200 chars)
- status: Enum (PENDING, COMPLETED)
- created_at: DateTime
- updated_at: DateTime

### Removed Over-Engineering
❌ **Removed** (YAGNI violations):
- description field
- due_date field
- priority levels
- display_order field
- PriorityLevel enum
- TaskList virtual entity

✅ **Kept** (Essential only):
- Unique identifier
- Task content
- Completion status
- Audit timestamps

### Validation Rules
- title: non-empty string, max length 200
- status: must be PENDING or COMPLETED
- id: auto-generated UUID
- timestamps: auto-managed

### State Transitions
- PENDING → COMPLETED
- COMPLETED → PENDING

## Implementation
Single SQLAlchemy model in todo-core library:

```python
class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

This follows constitutional simplicity: one model, no abstractions, framework used directly.