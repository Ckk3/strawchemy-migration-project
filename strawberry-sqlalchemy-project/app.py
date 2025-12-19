import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader

from database import create_tables, get_session
from schema import schema
import models

# Import exclusive feature schemas
from schema_relay import schema_with_relay
from schema_polymorphic import schema_with_polymorphic, Content, Article, Video


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


def seed_polymorphic_data():
    """Seed polymorphic content data for demo."""
    from database import Base, engine
    import uuid

    # Create the content table if it doesn't exist
    Content.__table__.create(engine, checkfirst=True)

    session = get_session()

    # Check if content data already exists
    if session.query(Content).first():
        session.close()
        return

    # Create sample content
    content_items = [
        Article(
            id=str(uuid.uuid4()),
            title="Introduction to GraphQL",
            body="GraphQL is a query language for APIs...",
            author="Alice Johnson",
        ),
        Article(
            id=str(uuid.uuid4()),
            title="SQLAlchemy Best Practices",
            body="When working with SQLAlchemy...",
            author="Bob Smith",
        ),
        Video(
            id=str(uuid.uuid4()),
            title="GraphQL Tutorial",
            body="Learn GraphQL from scratch",
            duration_seconds="3600",
        ),
        Video(
            id=str(uuid.uuid4()),
            title="Python Advanced Features",
            body="Deep dive into Python",
            duration_seconds="5400",
        ),
    ]
    session.add_all(content_items)
    session.commit()
    session.close()


async def get_context():
    """Get GraphQL context with SQLAlchemy loader."""
    session = get_session()
    return {
        "sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session),
    }


# Initialize database and seed data on startup
create_tables()
seed_data()
seed_polymorphic_data()

app = FastAPI(
    title="Strawberry-SQLAlchemy-Mapper Demo API",
    description="""
    This API demonstrates strawberry-sqlalchemy-mapper's exclusive features for GraphQL + SQLAlchemy integration.
    
    ## Available Endpoints
    
    - `/graphql` - Main schema (basic queries)
    - `/graphql/relay` - Relay-style cursor pagination
    - `/graphql/polymorphic` - Polymorphic type hierarchies
    """,
)

# Main schema
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# Exclusive feature schemas at separate endpoints
app.include_router(
    GraphQLRouter(schema_with_relay, context_getter=get_context),
    prefix="/graphql/relay",
    tags=["Relay Pagination"],
)

app.include_router(
    GraphQLRouter(schema_with_polymorphic, context_getter=get_context),
    prefix="/graphql/polymorphic",
    tags=["Polymorphic Types"],
)


@app.get("/")
async def root():
    """Root endpoint with links to all GraphQL endpoints."""
    return {
        "message": "Strawberry-SQLAlchemy-Mapper Demo API",
        "endpoints": {
            "main": "/graphql",
            "relay": "/graphql/relay",
            "polymorphic": "/graphql/polymorphic",
        },
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
