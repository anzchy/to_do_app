# Todo Application Constitution

## Core Principles

### I. Library-First Architecture
Every feature MUST be implemented as a standalone, independently testable library. No direct application code is permitted outside of library boundaries. Each library MUST serve a single, well-defined purpose and be self-contained with clear interfaces.

**Requirements:**
- Maximum 3 libraries total (todo-core, todo-cli, todo-api)
- Each library independently installable via pip
- No circular dependencies between libraries
- Clear separation of concerns: data/business logic, CLI interface, web interface

### II. CLI Interface Mandatory
Every library MUST expose functionality through a command-line interface supporting standard Unix conventions.

**Requirements:**
- `--help` flag with usage documentation
- `--version` flag showing semantic version
- `--format` flag supporting both human-readable and JSON output
- Exit codes: 0 (success), 1 (user error), 2 (system error)
- Stdin/stdout protocol: input via args/stdin, output to stdout, errors to stderr

### III. Test-First Development (NON-NEGOTIABLE)
All code MUST follow strict Test-Driven Development with RED-GREEN-REFACTOR cycle enforcement.

**Requirements:**
- Tests written BEFORE implementation code
- Every test MUST fail initially (RED phase verified)
- Implementation makes tests pass (GREEN phase)
- Code improved while maintaining tests (REFACTOR phase)
- Git commits MUST show test files before implementation files
- Test order: Contract → Integration → E2E → Unit

**Forbidden:**
- Implementation before tests
- Skipping RED phase verification
- Mock objects for integration tests (use real SQLite database)

### IV. Simplicity and Anti-Patterns
Embrace radical simplicity and avoid premature abstraction.

**Requirements:**
- Use frameworks directly without wrapper classes
- Single data model (Task) - no DTOs unless serialization differs
- No Repository pattern, Unit of Work, or similar abstractions
- No service layers unless proven necessary
- YAGNI principle strictly enforced

**Forbidden:**
- Over-engineering for imaginary future requirements
- Abstract base classes without concrete need
- Complex inheritance hierarchies
- Design patterns without proven necessity

### V. Real Dependencies
Use actual dependencies in tests and development to ensure realistic behavior.

**Requirements:**
- SQLite database for all testing levels
- Real file system operations
- Actual HTTP requests in integration tests
- No mocking of external dependencies unless absolutely necessary

### VI. Observability
All libraries MUST provide comprehensive observability for debugging and monitoring.

**Requirements:**
- Structured logging using Python logging module
- JSON log format for machine parsing
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Request tracing through web interface
- Error context with sufficient detail for debugging

### VII. Versioning and Breaking Changes
Strict semantic versioning with explicit handling of breaking changes.

**Requirements:**
- MAJOR.MINOR.BUILD format (e.g., 1.2.15)
- BUILD number increments on every code change
- MINOR increments for backward-compatible features
- MAJOR increments for breaking changes
- Breaking changes require migration plan and parallel testing

## Technical Standards

### Programming Language
- **Python 3.11+** exclusively
- Type hints mandatory for all public interfaces
- Black code formatting (line length: 88 characters)
- isort for import organization
- flake8 for linting (max complexity: 10)

### Frameworks and Libraries
- **todo-core**: SQLAlchemy 2.0+, Click 8.0+
- **todo-cli**: Click 8.0+, Rich for output formatting
- **todo-api**: FastAPI 0.100+, Jinja2 3.1+, HTMX 1.9+
- **Database**: SQLite 3.35+ (development/testing), PostgreSQL 14+ (production)
- **Testing**: pytest 7.0+, pytest-asyncio, playwright (E2E)

### Code Organization
```
<library-name>/
├── src/
│   └── <library_name>/
│       ├── __init__.py
│       ├── models.py       # Data models (todo-core only)
│       ├── operations.py   # Business logic (todo-core only)
│       ├── cli.py         # CLI interface
│       └── main.py        # Application entry (todo-api only)
├── tests/
│   ├── contract/          # API contract tests
│   ├── integration/       # Cross-library tests
│   ├── e2e/              # End-to-end tests
│   └── unit/             # Unit tests
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

### Database Standards
- **Schema**: Simple, normalized design without premature optimization
- **Migrations**: Alembic for schema changes, backward compatible
- **Queries**: SQLAlchemy Core for complex queries, ORM for simple operations
- **Transactions**: Explicit transaction boundaries, rollback on errors
- **Connection Pool**: SQLAlchemy defaults, no custom pooling

### API Design
- **REST principles**: Resource-based URLs, HTTP verbs for actions
- **Content types**: JSON for APIs, HTML for web interface
- **Error handling**: Consistent error responses with details
- **Validation**: Pydantic models for request/response validation
- **Documentation**: OpenAPI/Swagger automatic generation

### Frontend Standards
- **Architecture**: Server-side rendering with HTMX for interactivity
- **Templates**: Jinja2 with inheritance, minimal JavaScript
- **Styling**: TailwindCSS utility classes, responsive design
- **Forms**: Standard HTML forms with HTMX enhancements
- **Assets**: Served directly, no build pipeline required

## Quality Gates

### Pre-Commit Requirements
- All tests pass (pytest exit code 0)
- Code formatting verified (black --check)
- Linting passes (flake8 with zero violations)
- Type checking passes (mypy --strict)
- Test coverage ≥ 90% for modified files

### Code Review Requirements
- Constitutional compliance verified
- TDD evidence in commit history
- No over-engineering or premature optimization
- Clear, self-documenting code
- Appropriate test coverage

### Integration Requirements
- Contract tests validate API specifications
- Integration tests verify library interactions
- E2E tests confirm user workflows
- Performance benchmarks within acceptable ranges
- Security scan passes (bandit)

## Development Workflow

### Branch Strategy
- **main**: Production-ready code only
- **feature/<ticket>**: Individual features following constitution
- **hotfix/<issue>**: Critical production fixes
- No long-lived development branches

### Commit Standards
- Conventional commits format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Clear, imperative mood descriptions
- Reference issue/ticket numbers where applicable

### Release Process
1. Version bump in pyproject.toml
2. CHANGELOG.md update with breaking changes
3. Tag release with semantic version
4. Build and publish packages to PyPI
5. Deploy to production environments

## Security Requirements

### Input Validation
- All user inputs validated using Pydantic models
- SQL injection prevention through parameterized queries
- XSS prevention through template auto-escaping
- CSRF protection for state-changing operations

### Authentication & Authorization
- Placeholder for future authentication system
- Session management through secure cookies
- Role-based access control framework ready
- Password hashing with bcrypt when implemented

### Data Protection
- No sensitive data in logs
- Environment variables for configuration
- Secrets management through external systems
- Regular dependency vulnerability scanning

## Performance Standards

### Response Time Targets
- **API endpoints**: < 100ms p95 response time
- **Database queries**: < 50ms for simple operations
- **Page loads**: < 200ms first contentful paint
- **CLI commands**: < 500ms for typical operations

### Scalability Considerations
- Database connection pooling configured
- Async operations where beneficial
- Horizontal scaling capability maintained
- Stateless application design

### Resource Limits
- **Memory usage**: < 100MB per process
- **Database connections**: < 10 per application instance
- **File handles**: Properly closed, no leaks
- **CPU usage**: < 50% under normal load

## Governance

### Constitutional Authority
This constitution supersedes all other development practices, guidelines, and preferences. All code reviews, architectural decisions, and implementation choices MUST comply with constitutional requirements.

### Amendment Process
1. Proposed changes documented with rationale
2. Impact assessment on existing code
3. Migration plan for breaking changes
4. Team consensus required for approval
5. Version increment and effective date specified

### Violation Handling
- **Minor violations**: Immediate correction required
- **Major violations**: Code review rejection, rewrite necessary
- **Repeated violations**: Escalation to technical leadership
- **Constitutional challenges**: Formal amendment process required

### Compliance Verification
- Automated checks in CI/CD pipeline
- Manual review during code review process
- Periodic constitutional compliance audits
- Training for new team members on constitutional requirements

---

**Version**: 1.0.0 | **Ratified**: 2025-09-14 | **Last Amended**: 2025-09-14

*This constitution serves as the foundational governance for the Todo Application project. All implementation decisions must align with these principles to ensure consistency, quality, and maintainability.*