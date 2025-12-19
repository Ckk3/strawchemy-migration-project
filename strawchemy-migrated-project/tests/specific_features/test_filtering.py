"""Tests for strawchemy filtering feature (EXCLUSIVE to strawchemy)."""

import pytest

from schema_filters import schema_with_filters


class TestFiltering:
    """Test filtering capabilities."""

    @pytest.fixture
    def execute_query(self, graphql_context):
        async def _execute(query: str):
            return await schema_with_filters.execute(
                query, context_value=graphql_context
            )

        return _execute

    @pytest.mark.asyncio
    async def test_filter_by_exact_name(self, sample_data, execute_query):
        query = """
            query {
                employeesFiltered(filter: { name: { eq: "Alice Johnson" } }) {
                    name
                    email
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        assert len(result.data["employeesFiltered"]) == 1
        assert result.data["employeesFiltered"][0]["name"] == "Alice Johnson"

    @pytest.mark.asyncio
    async def test_filter_by_contains(self, sample_data, execute_query):
        query = """
            query {
                employeesFiltered(filter: { name: { contains: "Johnson" } }) {
                    name
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        assert len(result.data["employeesFiltered"]) == 1
        assert "Johnson" in result.data["employeesFiltered"][0]["name"]

    @pytest.mark.asyncio
    async def test_filter_by_email_endswith(self, sample_data, execute_query):
        query = """
            query {
                employeesFiltered(filter: { email: { endswith: "@example.com" } }) {
                    email
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        # All employees have @example.com emails
        assert len(result.data["employeesFiltered"]) == 3

    @pytest.mark.asyncio
    async def test_filter_departments_by_name(self, sample_data, execute_query):
        query = """
            query {
                departmentsFiltered(filter: { name: { eq: "Engineering" } }) {
                    name
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        assert len(result.data["departmentsFiltered"]) == 1
        assert result.data["departmentsFiltered"][0]["name"] == "Engineering"

    @pytest.mark.asyncio
    async def test_filter_no_results(self, sample_data, execute_query):
        query = """
            query {
                employeesFiltered(filter: { name: { eq: "Nonexistent Person" } }) {
                    name
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        assert len(result.data["employeesFiltered"]) == 0
