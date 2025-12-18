import strawberry
from strawchemy import Strawchemy, StrawchemyConfig

import models


# Custom session getter that works with dict context
def get_session(info: strawberry.Info):
    return info.context["session"]


# Initialize strawchemy with SQLite dialect and custom session getter
strawchemy = Strawchemy(
    StrawchemyConfig(
        dialect="sqlite",
        session_getter=get_session,
    )
)


@strawchemy.type(models.Department, include="all")
class DepartmentType:
    """GraphQL type for Department model."""

    pass


@strawchemy.type(models.Employee, exclude=["password_hash"], override=True)
class EmployeeType:
    """GraphQL type for Employee model.

    Note: password_hash is excluded from the GraphQL schema for security.
    """

    pass


@strawberry.type
class Query:
    # Strawchemy generates resolvers automatically
    departments: list[DepartmentType] = strawchemy.field()
    employees: list[EmployeeType] = strawchemy.field()


schema = strawberry.Schema(query=Query)
