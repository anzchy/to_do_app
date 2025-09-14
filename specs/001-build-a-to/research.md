# Research Findings

## Technical Stack Decisions

### Backend Framework
**Decision**: FastAPI
**Rationale**:
- High performance async framework
- Automatic OpenAPI documentation
- Built-in request/response validation
- Strong typing support with Pydantic
- Active community and good documentation
**Alternatives considered**:
- Flask: Less built-in functionality for APIs
- Django: Too heavyweight for this MVP
- Starlette: Lower level, FastAPI provides better developer experience

### Frontend Framework
**Decision**: HTMX + Jinja2
**Rationale**:
- Server-side rendering with Jinja2 templates
- HTMX for dynamic UI updates without JavaScript
- Direct integration with FastAPI
- Simple deployment and maintenance
- Excellent performance characteristics
**Alternatives considered**:
- React: More complex, requires separate build process
- Streamlit: Limited customization, not ideal for complex UIs
- Dash: Better for data visualization apps
- Justpy: Smaller community, less mature

### Database
**Decision**: SQLite
**Rationale**:
- Specified in requirements for MVP
- File-based, no separate server needed
- Supports all needed features (CRUD, sorting)
- Easy to migrate to PostgreSQL later if needed
**Alternatives considered**:
- PostgreSQL: Better for production but overscoped for MVP
- MongoDB: Relational data better fits SQL model

### ORM
**Decision**: SQLAlchemy
**Rationale**:
- Industry standard Python ORM
- Works well with FastAPI via FastAPI-SQLAlchemy
- Strong typing support
- Migration support via Alembic
**Alternatives considered**:
- Tortoise ORM: Async but less mature
- Peewee: Simpler but fewer features

### UI Components
**Decision**: TailwindCSS + Sortable.js
**Rationale**:
- TailwindCSS for utility-first styling
- Sortable.js for drag-and-drop functionality
- Works well with HTMX
- No build process needed
**Alternatives considered**:
- Bootstrap: More opinionated, heavier
- Custom CSS: More maintenance overhead

## Best Practices Research

### FastAPI Best Practices
- Use Pydantic models for request/response validation
- Implement dependency injection for services
- Use async/await for database operations
- Structure routes by resource type
- Use FastAPI built-in error handling

### HTMX Best Practices
- Use hx-swap for dynamic content updates
- Implement proper loading states
- Use hx-trigger for custom events
- Structure templates for partial updates
- Follow progressive enhancement

### Jinja2 Best Practices
- Use template inheritance
- Implement proper template organization
- Use macros for reusable components
- Keep logic in Python code
- Cache templates in production

### SQLAlchemy Best Practices
- Use declarative models
- Implement migrations with Alembic
- Use session management via dependency injection
- Implement proper transaction handling
- Use relationship loading strategies appropriately

## Performance Considerations
- Use template caching
- Implement proper database indexes
- Use partial page updates with HTMX
- Optimize Sortable.js operations
- Use async operations where beneficial
- Implement proper HTTP caching

## Security Considerations
- Implement CSRF protection
- Sanitize user input
- Use parameterized queries
- Plan for future authentication integration
- Implement proper error handling
- Use secure headers

## Testing Strategy
- Use pytest for backend testing
- Implement API contract tests
- Use playwright for frontend testing
- Integration tests for critical flows
- End-to-end tests for key user journeys
- Test HTMX interactions