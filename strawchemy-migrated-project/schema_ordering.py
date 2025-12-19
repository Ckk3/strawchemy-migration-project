"""
STRAWCHEMY EXCLUSIVE FEATURE: Ordering

This feature is NOT available in strawberry-sqlalchemy-mapper.

Documentation: https://github.com/gazorby/strawchemy#resolver-generation
"""

import strawberry

import models
from schema import strawchemy, EmployeeType, DepartmentType


# Order inputs define which fields can be used for sorting (ASC/DESC)
@strawchemy.order(models.Employee, include="all", override=True)
class EmployeeOrderBy:
    pass


@strawchemy.order(models.Department, include="all", override=True)
class DepartmentOrderBy:
    pass


@strawberry.type
class QueryWithOrdering:
    employees_ordered: list[EmployeeType] = strawchemy.field(order_by=EmployeeOrderBy)
    departments_ordered: list[DepartmentType] = strawchemy.field(
        order_by=DepartmentOrderBy
    )


schema_with_ordering = strawberry.Schema(query=QueryWithOrdering)
