# Implementation Plan: Todo List Application (Constitutional)

**Branch**: `001-build-a-to` | **Date**: 2025-09-14 | **Spec**: [spec.md](spec.md)

## Summary
Build a simple todo list as 3 separate libraries following constitutional principles.

## Technical Context
**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLAlchemy, Jinja2
**Storage**: SQLite
**Testing**: pytest
**Target Platform**: CLI + Web
**Project Type**: 3 libraries (max allowed)
**Performance Goals**: < 100ms response time
**Constraints**: Constitutional compliance
**Scale/Scope**: Single-user MVP

## Constitution Check ✅

**Simplicity**:
- Projects: 3 (todo-core, todo-api, todo-cli) ✅
- Using framework directly? Yes ✅
- Single data model? Yes ✅
- Avoiding patterns? Yes ✅

**Architecture**:
- EVERY feature as library? Yes ✅
- Libraries listed:
  - todo-core: Task data model and business logic
  - todo-api: Web interface (FastAPI + HTMX)
  - todo-cli: Command-line interface
- CLI per library: Yes ✅
- Library docs: Yes ✅

**Testing**:
- RED-GREEN-Refactor cycle enforced? Yes ✅
- All other testing requirements: Yes ✅

**Observability**: Yes ✅
**Versioning**: Yes (0.1.0) ✅

## Project Structure (Constitutional)

### 3 Libraries
```
todo-core/           # Library 1: Core business logic
├── src/
│   ├── models.py    # Task model only
│   └── operations.py # CRUD operations
├── tests/
└── cli.py           # todo-core --help

todo-api/            # Library 2: Web interface
├── src/
│   ├── main.py      # FastAPI app
│   └── templates/   # Simple HTMX templates
├── tests/
└── cli.py           # todo-api --help

todo-cli/            # Library 3: Command-line interface
├── src/
│   └── cli.py       # Full CLI implementation
├── tests/
└── cli.py           # todo-cli --help
```

## Simplified Requirements

### Core Library (todo-core)
- Task model: id, title, status, created_at
- Operations: create, list, update, delete
- CLI: `todo-core list --format=json`

### API Library (todo-api)
- 4 endpoints: GET/POST/PUT/DELETE /tasks
- 2 templates: list.html, form.html
- CLI: `todo-api serve --port=8000`

### CLI Library (todo-cli)
- Commands: add, list, done, rm
- Text-based interface
- CLI: `todo-cli add "Buy milk"`

## Removed Over-Engineering

❌ **Removed**:
- Complex service layers
- Priority levels (YAGNI)
- Drag-and-drop (over-complex for MVP)
- Due dates (YAGNI)
- Sorting/filtering (YAGNI)
- 9 documentation files → 3 simple ones
- Template specifications → basic templates
- Implementation guides → follow TDD

✅ **Kept**:
- Simple CRUD operations
- Basic web interface
- CLI interface
- Constitutional compliance

## Implementation Order

1. **todo-core** (Library 1)
   - Write failing tests for Task model
   - Implement Task model
   - Write failing tests for operations
   - Implement CRUD operations
   - Add CLI interface

2. **todo-cli** (Library 3)
   - Write failing tests for CLI commands
   - Implement CLI using todo-core
   - Add CLI interface

3. **todo-api** (Library 2)
   - Write failing contract tests
   - Implement API endpoints using todo-core
   - Add basic HTMX templates
   - Add CLI interface

## Progress Tracking

**Phase Status**:
- [x] Phase 0: Constitutional compliance verified
- [x] Phase 1: Simplified design complete
- [x] Phase 2: 3-library approach planned
- [ ] Phase 3: Tasks generated
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Constitutional Gates**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] Over-engineering removed
- [x] 3-library structure confirmed