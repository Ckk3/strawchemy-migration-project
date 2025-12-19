"""
STRAWCHEMY EXCLUSIVE FEATURE: Filtering

This feature is NOT available in strawberry-sqlalchemy-mapper.

Documentation: https://github.com/gazorby/strawchemy#filtering
"""

import strawberry

import models
from schema import strawchemy, EmployeeType, DepartmentType


# Use include="all" to allow filtering on all fields, or specify a list
@strawchemy.filter(models.Employee, include="all", override=True)
class EmployeeFilter:
    pass


@strawchemy.filter(models.Department, include="all", override=True)
class DepartmentFilter:
    pass


@strawberry.type
class QueryWithFilters:
    employees_filtered: list[EmployeeType] = strawchemy.field(
        filter_input=EmployeeFilter
    )
    departments_filtered: list[DepartmentType] = strawchemy.field(
        filter_input=DepartmentFilter
    )


schema_with_filters = strawberry.Schema(query=QueryWithFilters)
