import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from database import create_tables, get_session
from schema import schema
import models

# Import exclusive feature schemas
from schema_filters import schema_with_filters
from schema_ordering import schema_with_ordering
from schema_pagination import schema_with_pagination, schema_with_child_pagination
from schema_aggregations import (
    schema_with_relationship_aggregations,
    schema_with_root_aggregations,
)
from schema_mutations import schema_with_mutations


def seed_data():
    """Seed the database with sample data."""
    session = get_session()

    # Check if data already exists
    if session.query(models.Department).first():
        session.close()
        return

    # Create departments
    engineering = models.Department(name="Engineering")
    marketing = models.Department(name="Marketing")
    hr = models.Department(name="Human Resources")
    session.add_all([engineering, marketing, hr])
    session.flush()

    # Create employees
    employees = [
        models.Employee(
            name="Alice Johnson",
            email="alice@example.com",
            password_hash="hashed_password_1",
            department_id=engineering.id,
        ),
        models.Employee(
            name="Bob Smith",
            email="bob@example.com",
            password_hash="hashed_password_2",
            department_id=engineering.id,
        ),
        models.Employee(
            name="Carol Williams",
            email="carol@example.com",
            password_hash="hashed_password_3",
            department_id=marketing.id,
        ),
        models.Employee(
            name="David Brown",
            email="david@example.com",
            password_hash="hashed_password_4",
            department_id=marketing.id,
        ),
        models.Employee(
            name="Eve Davis",
            email="eve@example.com",
            password_hash="hashed_password_5",
            department_id=hr.id,
        ),
    ]
    session.add_all(employees)
    session.commit()
    session.close()


async def get_context():
    """Get GraphQL context with SQLAlchemy session.

    Strawchemy retrieves the session via info.context["session"]
    using a custom session_getter configured in StrawchemyConfig.
    """
    return {"session": get_session()}


# Initialize database and seed data on startup
create_tables()
seed_data()

app = FastAPI(
    title="Strawchemy Demo API",
    description="""
    This API demonstrates strawchemy's exclusive features for GraphQL + SQLAlchemy integration.
    
    ## Available Endpoints
    
    - `/graphql` - Main schema (basic queries)
    - `/graphql/filters` - Filtering examples
    - `/graphql/ordering` - Ordering examples
    - `/graphql/pagination` - Offset pagination examples
    - `/graphql/aggregations` - Aggregation examples
    - `/graphql/mutations` - CRUD mutation examples
    """,
)

# Main schema
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# Exclusive feature schemas at separate endpoints
app.include_router(
    GraphQLRouter(schema_with_filters, context_getter=get_context),
    prefix="/graphql/filters",
    tags=["Filtering"],
)

app.include_router(
    GraphQLRouter(schema_with_ordering, context_getter=get_context),
    prefix="/graphql/ordering",
    tags=["Ordering"],
)

app.include_router(
    GraphQLRouter(schema_with_pagination, context_getter=get_context),
    prefix="/graphql/pagination",
    tags=["Pagination"],
)

app.include_router(
    GraphQLRouter(schema_with_root_aggregations, context_getter=get_context),
    prefix="/graphql/aggregations",
    tags=["Aggregations"],
)

app.include_router(
    GraphQLRouter(schema_with_mutations, context_getter=get_context),
    prefix="/graphql/mutations",
    tags=["Mutations"],
)


@app.get("/")
async def root():
    """Root endpoint with links to all GraphQL endpoints."""
    return {
        "message": "Strawchemy Demo API",
        "endpoints": {
            "main": "/graphql",
            "filters": "/graphql/filters",
            "ordering": "/graphql/ordering",
            "pagination": "/graphql/pagination",
            "aggregations": "/graphql/aggregations",
            "mutations": "/graphql/mutations",
        },
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
