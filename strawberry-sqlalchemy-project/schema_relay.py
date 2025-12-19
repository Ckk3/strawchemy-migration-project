"""
STRAWBERRY-SQLALCHEMY-MAPPER EXCLUSIVE FEATURE: Relay-Style Pagination

This feature is NOT available in strawchemy.
(strawchemy uses offset pagination instead)

Documentation: https://relay.dev/graphql/connections.htm
"""

from typing import List, Optional
import base64
import strawberry
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
from sqlalchemy import select

import models
from database import get_session


strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


@strawberry_sqlalchemy_mapper.type(models.Department)
class DepartmentType:
    pass


@strawberry_sqlalchemy_mapper.type(models.Employee)
class EmployeeType:
    __exclude__ = ["password_hash"]


# Relay connection types follow the Relay Connection Specification
@strawberry.type
class RelayPageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str] = None
    end_cursor: Optional[str] = None


@strawberry.type
class DepartmentRelayEdge:
    cursor: str
    node: DepartmentType


@strawberry.type
class DepartmentRelayConnection:
    edges: List[DepartmentRelayEdge]
    page_info: RelayPageInfo


@strawberry.type
class EmployeeRelayEdge:
    cursor: str
    node: EmployeeType


@strawberry.type
class EmployeeRelayConnection:
    edges: List[EmployeeRelayEdge]
    page_info: RelayPageInfo


def encode_cursor(index: int) -> str:
    return base64.b64encode(f"cursor:{index}".encode()).decode()


def decode_cursor(cursor: str) -> int:
    decoded = base64.b64decode(cursor.encode()).decode()
    return int(decoded.split(":")[1])


@strawberry.type
class QueryWithRelay:
    @strawberry.field
    def departments_connection(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        last: Optional[int] = None,
        before: Optional[str] = None,
    ) -> DepartmentRelayConnection:
        session = get_session()
        all_departments = list(session.scalars(select(models.Department)).all())

        start_idx = 0
        if after:
            start_idx = decode_cursor(after) + 1

        end_idx = len(all_departments)
        if first is not None:
            end_idx = min(start_idx + first, len(all_departments))

        departments_slice = all_departments[start_idx:end_idx]

        edges = [
            DepartmentRelayEdge(cursor=encode_cursor(start_idx + i), node=dept)
            for i, dept in enumerate(departments_slice)
        ]

        page_info = RelayPageInfo(
            has_next_page=end_idx < len(all_departments),
            has_previous_page=start_idx > 0,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        )

        return DepartmentRelayConnection(edges=edges, page_info=page_info)

    @strawberry.field
    def employees_connection(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
    ) -> EmployeeRelayConnection:
        session = get_session()
        all_employees = list(session.scalars(select(models.Employee)).all())

        start_idx = 0
        if after:
            start_idx = decode_cursor(after) + 1

        end_idx = len(all_employees)
        if first is not None:
            end_idx = min(start_idx + first, len(all_employees))

        employees_slice = all_employees[start_idx:end_idx]

        edges = [
            EmployeeRelayEdge(cursor=encode_cursor(start_idx + i), node=emp)
            for i, emp in enumerate(employees_slice)
        ]

        page_info = RelayPageInfo(
            has_next_page=end_idx < len(all_employees),
            has_previous_page=start_idx > 0,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        )

        return EmployeeRelayConnection(edges=edges, page_info=page_info)

    @strawberry.field
    def departments(self) -> List[DepartmentType]:
        session = get_session()
        return list(session.scalars(select(models.Department)).all())

    @strawberry.field
    def employees(self) -> List[EmployeeType]:
        session = get_session()
        return list(session.scalars(select(models.Employee)).all())


strawberry_sqlalchemy_mapper.finalize()
additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())

schema_with_relay = strawberry.Schema(
    query=QueryWithRelay,
    types=additional_types,
)
