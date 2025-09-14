# Data Models

## Task
The core entity representing a todo item.

### Fields
- id: UUID (primary key)
- title: String (required)
- description: String (optional)
- due_date: DateTime (optional)
- priority: Enum(PriorityLevel)
- status: Enum(TaskStatus)
- display_order: Integer
- created_at: DateTime
- updated_at: DateTime

### Validation Rules
- title: non-empty string, max length 200
- description: max length 1000
- due_date: must be future date when creating/updating
- priority: must be valid PriorityLevel
- status: must be valid TaskStatus
- display_order: non-negative integer

### State Transitions
- Status transitions:
  * PENDING -> COMPLETED
  * COMPLETED -> PENDING
- No other field transitions have special rules

## PriorityLevel
Enumeration for task priority levels.

### Values
- HIGH
- MEDIUM
- LOW

### Validation Rules
- Must be one of the defined values
- Cannot be null

## TaskStatus
Enumeration for task completion status.

### Values
- PENDING
- COMPLETED

### Validation Rules
- Must be one of the defined values
- Cannot be null

## TaskList
Virtual entity representing an ordered collection of tasks.

### Composition
- Collection of Task entities
- Ordering defined by Task.display_order

### Operations
- Reordering: Updates display_order of affected tasks
- Filtering: By status, priority
- Sorting: By due_date, priority, display_order

### Validation Rules
- display_order values must be unique within list
- No gaps allowed in display_order sequence

## Relationships
- Task -> PriorityLevel: Many-to-One
- Task -> TaskStatus: Many-to-One
- TaskList -> Task: One-to-Many (virtual relationship via display_order)