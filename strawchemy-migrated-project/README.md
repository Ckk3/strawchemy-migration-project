# Strawchemy Migrated Project

A GraphQL API using [Strawberry](https://strawberry.rocks/) with [strawchemy](https://github.com/gazorby/strawchemy) for automatic type generation from SQLAlchemy models.

This project was migrated from `strawberry-sqlalchemy-mapper` to `strawchemy`.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Setup

1. Navigate to the project directory:
   ```bash
   cd strawchemy-migrated-project
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the application:
   ```bash
   uv run python app.py
   ```

4. Open the GraphQL playground at http://localhost:8000/graphql

## Project Structure

```
├── app.py          # FastAPI application with GraphQL endpoint
├── database.py     # SQLite database configuration
├── models.py       # SQLAlchemy models (Employee, Department)
├── schema.py       # Strawchemy GraphQL schema
├── pyproject.toml  # Project dependencies
└── tests/          # Test suite
    ├── conftest.py     # Pytest fixtures
    ├── test_schema.py  # GraphQL schema validation tests
    └── test_queries.py # GraphQL query tests
```

## Example Queries

### Get all employees
```graphql
{
  employees {
    id
    name
    email
  }
}
```

### Get all departments
```graphql
{
  departments {
    id
    name
  }
}
```

### Get employees with their department (nested relationship)
```graphql
{
  employees {
    id
    name
    email
    department {
      id
      name
    }
  }
}
```

### Get departments with employees
```graphql
{
  departments {
    id
    name
    employees {
      id
      name
      email
    }
  }
}
```

### Deeply nested query
```graphql
{
  departments {
    name
    employees {
      name
      department {
        name
      }
    }
  }
}
```

## Testing with cURL

```bash
# Get all employees
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ employees { id name email } }"}'

# Get all departments
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ departments { id name } }"}'

# Get employees with department
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ employees { name email department { name } } }"}'

# Get departments with employees
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ departments { name employees { name email } } }"}'
```

## Features Demonstrated

- **Strawchemy Type Generation**: Automatically generates Strawberry types from SQLAlchemy models using `@strawchemy.type()`
- **Field Exclusion**: Hides sensitive fields (e.g., `password_hash`) using `exclude=["password_hash"]` parameter
- **Automatic Resolvers**: Uses `strawchemy.field()` for automatic query resolution
- **Relationships**: Bidirectional relationships between Employee and Department
- **Session Context**: Session is provided via `info.context.session` (strawchemy default)

## Breaking Changes from strawberry-sqlalchemy-mapper

### Relay-style Connections Not Supported

The previous implementation using `strawberry-sqlalchemy-mapper` used Relay-style pagination for list relationships:

```graphql
# OLD - This will NOT work with strawchemy
{
  departments {
    employees {
      edges {
        node {
          id
          name
        }
      }
    }
  }
}
```

**Strawchemy uses simple lists instead:**

```graphql
# NEW - Use this with strawchemy
{
  departments {
    employees {
      id
      name
    }
  }
}
```

If you need pagination, strawchemy supports offset-based pagination which can be enabled via `strawchemy.field(pagination=True)`.

## Migration Summary

| Aspect | Before (strawberry-sqlalchemy-mapper) | After (strawchemy) |
|--------|---------------------------------------|-------------------|
| Mapper init | `StrawberrySQLAlchemyMapper()` | `Strawchemy("sqlite")` |
| Type decorator | `@mapper.type(Model)` | `@strawchemy.type(Model, include="all")` |
| Field exclusion | `__exclude__ = ["field"]` | `exclude=["field"]` parameter |
| Query fields | Manual `@strawberry.field` | `strawchemy.field()` |
| Finalization | `mapper.finalize()` required | Not needed |
| Data loader | `StrawberrySQLAlchemyLoader` in context | Built-in (automatic) |
| Session context | `sqlalchemy_loader` | `session` |
| List relationships | Relay connections | Simple lists |

## Testing

Install dev dependencies and run tests:

```bash
uv sync --extra dev
uv run pytest -v
```

### Test Suite

| File | Tests | Description |
|------|-------|-------------|
| `test_schema.py` | 8 | GraphQL schema types, field validation, `password_hash` exclusion |
| `test_queries.py` | 8 | GraphQL queries, nested relationships |
