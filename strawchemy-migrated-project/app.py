import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from database import create_tables, get_session
from schema import schema
import models


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
    session.add_all([engineering, marketing])
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

app = FastAPI()

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
