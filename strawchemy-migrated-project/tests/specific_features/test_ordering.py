"""Tests for strawchemy ordering feature (EXCLUSIVE to strawchemy)."""

import pytest

from schema_ordering import schema_with_ordering


class TestOrdering:
    """Test ordering capabilities."""

    @pytest.fixture
    def execute_query(self, graphql_context):
        async def _execute(query: str):
            return await schema_with_ordering.execute(
                query, context_value=graphql_context
            )

        return _execute

    @pytest.mark.asyncio
    async def test_order_employees_by_name_asc(self, sample_data, execute_query):
        query = """
            query {
                employeesOrdered(orderBy: { name: ASC }) {
                    name
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        names = [e["name"] for e in result.data["employeesOrdered"]]
        assert names == sorted(names)

    @pytest.mark.asyncio
    async def test_order_employees_by_name_desc(self, sample_data, execute_query):
        query = """
            query {
                employeesOrdered(orderBy: { name: DESC }) {
                    name
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        names = [e["name"] for e in result.data["employeesOrdered"]]
        assert names == sorted(names, reverse=True)

    @pytest.mark.asyncio
    async def test_order_employees_by_email_asc(self, sample_data, execute_query):
        query = """
            query {
                employeesOrdered(orderBy: { email: ASC }) {
                    email
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        emails = [e["email"] for e in result.data["employeesOrdered"]]
        assert emails == sorted(emails)

    @pytest.mark.asyncio
    async def test_order_departments_by_name_asc(self, sample_data, execute_query):
        query = """
            query {
                departmentsOrdered(orderBy: { name: ASC }) {
                    name
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        names = [d["name"] for d in result.data["departmentsOrdered"]]
        assert names == sorted(names)
