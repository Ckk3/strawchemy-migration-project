"""
STRAWCHEMY EXCLUSIVE FEATURE: Aggregations

This feature is NOT available in strawberry-sqlalchemy-mapper.

Documentation: https://github.com/gazorby/strawchemy#aggregations
"""

import strawberry

import models
from schema import strawchemy, EmployeeType, DepartmentType
from schema_filters import DepartmentFilter


# Strawchemy automatically adds aggregation fields for list relationships
# e.g., for `employees` relationship, it creates `employeesAggregate`
@strawberry.type
class QueryWithRelationshipAggregations:
    departments: list[DepartmentType] = strawchemy.field()


# Root aggregations allow aggregating at the query level
@strawchemy.aggregate(models.Employee, include="all", override=True)
class EmployeeAggregationType:
    pass


@strawchemy.aggregate(models.Department, include="all", override=True)
class DepartmentAggregationType:
    pass


@strawberry.type
class QueryWithRootAggregations:
    employees_aggregations: EmployeeAggregationType = strawchemy.field(
        root_aggregations=True
    )
    departments_aggregations: DepartmentAggregationType = strawchemy.field(
        root_aggregations=True
    )


# You can also filter by aggregations on relationships
@strawberry.type
class QueryFilterByAggregation:
    departments_filtered_by_aggregation: list[DepartmentType] = strawchemy.field(
        filter_input=DepartmentFilter
    )


schema_with_relationship_aggregations = strawberry.Schema(
    query=QueryWithRelationshipAggregations
)
schema_with_root_aggregations = strawberry.Schema(query=QueryWithRootAggregations)
schema_filter_by_aggregation = strawberry.Schema(query=QueryFilterByAggregation)
