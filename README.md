# Strawberry-SQLAlchemy to Strawchemy Migration Project

This project demonstrates migrating from `strawberry-sqlalchemy-mapper` to `strawchemy` - two libraries that integrate Strawberry GraphQL with SQLAlchemy.


## Feature Comparison

| Feature | strawberry-sqlalchemy-mapper | strawchemy |
|---------|:----------------------------:|:----------:|
| Type generation from models | Yes | Yes |
| Automatic resolvers | Limited | Yes |
| Field exclusion | Yes (`__exclude__`) | Yes (`exclude=[]`) |
| Relationship loading | Yes (via loader) | Yes |
| Secondary Tables Relationship | No | **NEED TO CHECK** |
| **Pagination** | | |
| Relay (cursor-based) | Yes | No |
| Offset pagination | No | Yes |
| **Querying** | | |
| Filtering | No | Yes |
| Ordering | No | Yes |
| Aggregations (count, sum, avg) | No | Yes |
| **Mutations** | | |
| Create (single/batch) | No | Yes |
| Update (by ID/filter) | No | Yes |
| Delete (all/filter) | No | Yes |
| Upsert | No | Yes |
| **Advanced** | | |
| Polymorphic types | Yes | **NEED TO CHECK** |
| Query hooks | No | Yes |
| Async support | Yes | Yes |
| `finalize()` required | Yes | No |

## Key Differences

### 1. Type Definition

**strawberry-sqlalchemy-mapper:**
```python
@mapper.type(models.Employee)
class Employee:
    __exclude__ = ["password_hash"]
```

**strawchemy:**
```python
@strawchemy.type(models.Employee, exclude=["password_hash"], override=True)
class EmployeeType:
    pass
```

### 2. Session Access

**strawberry-sqlalchemy-mapper:**
```python
from database import get_session

@strawberry.field
def employees(self) -> List[Employee]:
    session = get_session()
    return session.scalars(select(models.Employee)).all()
```

**strawchemy:**
```python
# Configure session getter once
def get_session(info: strawberry.Info):
    return info.context["session"]

strawchemy = Strawchemy(StrawchemyConfig(
    dialect="sqlite",
    session_getter=get_session,
))

# Fields are auto-resolved
employees: list[EmployeeType] = strawchemy.field()
```

### 3. Finalization

**strawberry-sqlalchemy-mapper:**
```python
# Required before creating schema
mapper.finalize()
additional_types = list(mapper.mapped_types.values())
schema = strawberry.Schema(query=Query, types=additional_types)
```

**strawchemy:**
```python
# No finalization needed
schema = strawberry.Schema(query=Query)
```

## Exclusive Features

### strawchemy Only

#### Filtering
```python
@strawchemy.filter(models.Employee, include="all")
class EmployeeFilter:
    pass

employees: list[EmployeeType] = strawchemy.field(filter_input=EmployeeFilter)
```

```graphql
query {
  employees(filter: { name: { contains: "John" } }) {
    name
    email
  }
}
```

#### Ordering
```python
@strawchemy.order(models.Employee, include="all")
class EmployeeOrderBy:
    pass

employees: list[EmployeeType] = strawchemy.field(order_by=EmployeeOrderBy)
```

```graphql
query {
  employees(orderBy: { name: ASC }) {
    name
  }
}
```

#### Offset Pagination
```python
employees: list[EmployeeType] = strawchemy.field(pagination=True)
```

```graphql
query {
  employees(offset: 0, limit: 10) {
    name
  }
}
```

#### Aggregations
```python
@strawchemy.aggregate(models.Employee, include="all")
class EmployeeAggregationType:
    pass

employees_aggregations: EmployeeAggregationType = strawchemy.field(root_aggregations=True)
```

```graphql
query {
  employeesAggregations {
    aggregations {
      count
      min { name }
      max { name }
    }
  }
}
```

#### CRUD Mutations
```python
@strawchemy.input(models.Employee, include=["name", "email"], mode="create_input")
class EmployeeCreateInput:
    pass

create_employee: EmployeeType = strawchemy.create(EmployeeCreateInput)
delete_employees: list[EmployeeType] = strawchemy.delete(EmployeeFilter)
```

### strawberry-sqlalchemy-mapper Only

#### Relay Pagination
```python
@strawberry.type
class EmployeeConnection(KeysetConnection[EmployeeType]):
    pass
```

```graphql
query {
  employeesConnection(first: 10, after: "cursor") {
    edges {
      cursor
      node { name }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

#### Polymorphic Types
```python
@mapper.interface(Content)
class ContentInterface:
    pass

@mapper.type(Article)
class ArticleType:
    pass

@mapper.type(Video)
class VideoType:
    pass
```

```graphql
query {
  allContent {
    __typename
    title
    ... on ArticleType {
      author
    }
    ... on VideoType {
      durationSeconds
    }
  }
}
```

## Running the Projects

## Project Structure

```
strawchemy-migration-project/
├── strawberry-sqlalchemy-project/   # Original implementation
│   ├── app.py                       # FastAPI app
│   ├── database.py                  # SQLite database config
│   ├── models.py                    # SQLAlchemy models
│   ├── schema.py                    # Main GraphQL schema
│   ├── schema_relay.py              # Relay pagination (EXCLUSIVE)
│   ├── schema_polymorphic.py        # Polymorphic types (EXCLUSIVE)
│   └── tests/
│
├── strawchemy-migrated-project/     # Migrated implementation
│   ├── app.py                       # FastAPI app
│   ├── database.py                  # SQLite database config
│   ├── models.py                    # SQLAlchemy models
│   ├── schema.py                    # Main GraphQL schema
│   ├── schema_filters.py            # Filtering (EXCLUSIVE)
│   ├── schema_ordering.py           # Ordering (EXCLUSIVE)
│   ├── schema_pagination.py         # Offset pagination (EXCLUSIVE)
│   ├── schema_aggregations.py       # Aggregations (EXCLUSIVE)
│   ├── schema_mutations.py          # CRUD mutations (EXCLUSIVE)
│   └── tests/
│
└── README.md                        # This file
```

### strawberry-sqlalchemy-project
```bash
cd strawberry-sqlalchemy-project
uv sync
uv run pytest        # Run tests
uv run uvicorn app:app --reload  # Start server
```

### strawchemy-migrated-project
```bash
cd strawchemy-migrated-project
uv sync
uv run pytest        # Run tests
uv run uvicorn app:app --reload  # Start server
```

## Migration Checklist

When migrating from `strawberry-sqlalchemy-mapper` to `strawchemy`:

1. [ ] Replace `StrawberrySQLAlchemyMapper` with `Strawchemy` instance
2. [ ] Update type decorators: `@mapper.type()` -> `@strawchemy.type()`
3. [ ] Change field exclusion from `__exclude__` to `exclude=[]` parameter
4. [ ] Add `override=True` to types that might conflict with auto-generated types
5. [ ] Remove `mapper.finalize()` call
6. [ ] Configure session getter in `StrawchemyConfig`
7. [ ] Replace manual resolvers with `strawchemy.field()`
8. [ ] If using Relay pagination, convert to offset pagination or implement custom
9. [ ] If using polymorphic types, implement manually or wait for strawchemy support

## Resources

- [strawchemy documentation](https://github.com/gazorby/strawchemy)
- [strawberry-sqlalchemy-mapper](https://github.com/strawberry-graphql/strawberry-sqlalchemy-mapper)
- [Strawberry GraphQL](https://strawberry.rocks/docs)
