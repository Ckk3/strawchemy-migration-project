from typing import List

import strawberry
from sqlalchemy import select
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

import models
from database import get_session

# Initialize the mapper
strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


@strawberry_sqlalchemy_mapper.type(models.Department)
class DepartmentType:
    pass


@strawberry_sqlalchemy_mapper.type(models.Employee)
class EmployeeType:
    # Exclude sensitive fields from the GraphQL schema
    __exclude__ = ["password_hash"]


@strawberry.type
class Query:
    @strawberry.field
    def departments(self) -> List[DepartmentType]:
        session = get_session()
        return session.scalars(select(models.Department)).all()

    @strawberry.field
    def employees(self) -> List[EmployeeType]:
        session = get_session()
        return session.scalars(select(models.Employee)).all()


# Finalize the mapper before creating the schema
strawberry_sqlalchemy_mapper.finalize()

# Get any additional types for polymorphic support
additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())

schema = strawberry.Schema(
    query=Query,
    types=additional_types,
)
