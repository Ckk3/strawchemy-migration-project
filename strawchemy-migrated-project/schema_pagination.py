"""
STRAWCHEMY EXCLUSIVE FEATURE: Offset Pagination

This feature is NOT available in strawberry-sqlalchemy-mapper.
(strawberry-sqlalchemy-mapper uses Relay-style cursor pagination instead)

Documentation: https://github.com/gazorby/strawchemy#pagination
"""

import strawberry

import models
from schema import strawchemy, EmployeeType, DepartmentType
from schema_filters import EmployeeFilter, DepartmentFilter
from schema_ordering import EmployeeOrderBy, DepartmentOrderBy


@strawberry.type
class QueryWithPagination:
    # Enable pagination with pagination=True (adds offset/limit params)
    employees_paginated: list[EmployeeType] = strawchemy.field(
        pagination=True,
        filter_input=EmployeeFilter,
        order_by=EmployeeOrderBy,
    )

    departments_paginated: list[DepartmentType] = strawchemy.field(
        pagination=True,
        filter_input=DepartmentFilter,
        order_by=DepartmentOrderBy,
    )


# child_pagination=True enables pagination on nested relationships
@strawchemy.type(models.Department, include="all", child_pagination=True)
class DepartmentTypeWithChildPagination:
    pass


@strawberry.type
class QueryWithChildPagination:
    departments_with_child_pagination: list[DepartmentTypeWithChildPagination] = (
        strawchemy.field()
    )


schema_with_pagination = strawberry.Schema(query=QueryWithPagination)
schema_with_child_pagination = strawberry.Schema(query=QueryWithChildPagination)
