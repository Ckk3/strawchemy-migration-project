# Strawberry SQLAlchemy Project

A simple GraphQL API using [Strawberry](https://strawberry.rocks/) with [strawberry-sqlalchemy-mapper](https://github.com/strawberry-graphql/strawberry-sqlalchemy) for automatic type generation from SQLAlchemy models.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Setup

1. Navigate to the project directory:
   ```bash
   cd strawberry-sqlalchemy-project
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
├── schema.py       # Strawberry GraphQL schema
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

### Get departments with employees (Relay-style pagination)
```graphql
{
  departments {
    id
    name
    employees {
      edges {
        node {
          id
          name
          email
        }
      }
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
      edges {
        node {
          name
          department {
            name
          }
        }
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

# Get departments with employees (Relay style)
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ departments { name employees { edges { node { name email } } } } }"}'
```

## Features Demonstrated

- **StrawberrySQLAlchemyMapper**: Automatically generates Strawberry types from SQLAlchemy models
- **`__exclude__`**: Hides sensitive fields (e.g., `password_hash`) from the GraphQL schema
- **Relationships**: Bidirectional relationships between Employee and Department
- **Relay Connections**: List relationships use Relay-style pagination by default

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
| `test_queries.py` | 8 | GraphQL queries, nested relationships, Relay pagination |

### Example Test Run

```bash
$ uv run pytest -v
======================== test session starts =========================
tests/test_queries.py::TestEmployeesQuery::test_employees_empty_database PASSED
tests/test_queries.py::TestEmployeesQuery::test_employees_returns_all PASSED
tests/test_queries.py::TestEmployeesQuery::test_employees_does_not_return_password_hash PASSED
tests/test_queries.py::TestDepartmentsQuery::test_departments_empty_database PASSED
tests/test_queries.py::TestDepartmentsQuery::test_departments_returns_all PASSED
tests/test_queries.py::TestNestedQueries::test_employees_with_department PASSED
tests/test_queries.py::TestNestedQueries::test_departments_with_employees PASSED
tests/test_queries.py::TestNestedQueries::test_deeply_nested_query PASSED
tests/test_schema.py::TestSchemaTypes::test_schema_has_query_type PASSED
tests/test_schema.py::TestSchemaTypes::test_query_has_employees_field PASSED
tests/test_schema.py::TestSchemaTypes::test_query_has_departments_field PASSED
tests/test_schema.py::TestEmployeeType::test_employee_has_expected_fields PASSED
tests/test_schema.py::TestEmployeeType::test_password_hash_is_excluded PASSED
tests/test_schema.py::TestDepartmentType::test_department_has_expected_fields PASSED
tests/test_schema.py::TestSchemaIntrospection::test_introspect_employee_fields PASSED
tests/test_schema.py::TestSchemaIntrospection::test_introspect_department_fields PASSED
========================= 16 passed in 0.37s =========================
```
