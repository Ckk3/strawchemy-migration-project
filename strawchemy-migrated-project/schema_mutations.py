"""
STRAWCHEMY EXCLUSIVE FEATURE: Mutations (CRUD Operations)

This feature is NOT available in strawberry-sqlalchemy-mapper.

Documentation: https://github.com/gazorby/strawchemy#mutations
"""

import strawberry

import models
from schema import strawchemy, EmployeeType, DepartmentType
from schema_filters import EmployeeFilter, DepartmentFilter


# Input types define which fields can be set during create/update operations
@strawchemy.input(
    models.Employee,
    include=["name", "email", "password_hash", "department_id"],
    mode="create_input",
)
class EmployeeCreateInput:
    pass


@strawchemy.input(
    models.Employee,
    include=["id", "name", "email", "department_id"],
    mode="update_by_pk_input",
)
class EmployeeUpdateInput:
    pass


@strawchemy.input(models.Department, include=["name"], mode="create_input")
class DepartmentCreateInput:
    pass


@strawchemy.input(models.Department, include=["id", "name"], mode="update_by_pk_input")
class DepartmentUpdateInput:
    pass


@strawberry.type
class Query:
    employees: list[EmployeeType] = strawchemy.field()
    departments: list[DepartmentType] = strawchemy.field()


@strawberry.type
class Mutation:
    # Create (single and batch)
    create_employee: EmployeeType = strawchemy.create(EmployeeCreateInput)
    create_department: DepartmentType = strawchemy.create(DepartmentCreateInput)
    create_employees: list[EmployeeType] = strawchemy.create(EmployeeCreateInput)
    create_departments: list[DepartmentType] = strawchemy.create(DepartmentCreateInput)

    # Update by primary key
    update_employee: EmployeeType = strawchemy.update_by_ids(EmployeeUpdateInput)
    update_department: DepartmentType = strawchemy.update_by_ids(DepartmentUpdateInput)

    # Update with filter
    update_employees_filtered: list[EmployeeType] = strawchemy.update(
        EmployeeUpdateInput, EmployeeFilter
    )

    # Delete with filter
    delete_employees: list[EmployeeType] = strawchemy.delete(EmployeeFilter)
    delete_departments: list[DepartmentType] = strawchemy.delete(DepartmentFilter)


schema_with_mutations = strawberry.Schema(query=Query, mutation=Mutation)
