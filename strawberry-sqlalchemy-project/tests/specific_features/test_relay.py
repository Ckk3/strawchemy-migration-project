"""Tests for Relay pagination feature (EXCLUSIVE to strawberry-sqlalchemy-mapper)."""

import pytest

from schema_relay import schema_with_relay


class TestRelayPagination:
    """Test Relay-style cursor pagination."""

    @pytest.fixture
    def execute_query(self, graphql_context):
        async def _execute(query: str):
            return await schema_with_relay.execute(query, context_value=graphql_context)

        return _execute

    @pytest.mark.asyncio
    async def test_departments_connection_returns_edges(
        self, sample_data, execute_query
    ):
        query = """
            query {
                departmentsConnection(first: 10) {
                    edges {
                        cursor
                        node {
                            name
                        }
                    }
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        edges = result.data["departmentsConnection"]["edges"]
        assert len(edges) == 2
        assert all("cursor" in edge for edge in edges)
        assert all("node" in edge for edge in edges)

    @pytest.mark.asyncio
    async def test_departments_connection_has_page_info(
        self, sample_data, execute_query
    ):
        query = """
            query {
                departmentsConnection(first: 1) {
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        startCursor
                        endCursor
                    }
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        page_info = result.data["departmentsConnection"]["pageInfo"]
        assert "hasNextPage" in page_info
        assert "hasPreviousPage" in page_info
        assert page_info["hasNextPage"] is True  # We have 2 departments, requested 1

    @pytest.mark.asyncio
    async def test_departments_connection_pagination_with_first(
        self, sample_data, execute_query
    ):
        query = """
            query {
                departmentsConnection(first: 1) {
                    edges {
                        node {
                            name
                        }
                    }
                    pageInfo {
                        hasNextPage
                    }
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        edges = result.data["departmentsConnection"]["edges"]
        assert len(edges) == 1
        assert result.data["departmentsConnection"]["pageInfo"]["hasNextPage"] is True

    @pytest.mark.asyncio
    async def test_employees_connection_returns_data(self, sample_data, execute_query):
        query = """
            query {
                employeesConnection(first: 5) {
                    edges {
                        cursor
                        node {
                            name
                            email
                        }
                    }
                    pageInfo {
                        hasNextPage
                    }
                }
            }
        """
        result = await execute_query(query)

        assert result.errors is None
        edges = result.data["employeesConnection"]["edges"]
        assert len(edges) == 3  # We have 3 employees
        assert result.data["employeesConnection"]["pageInfo"]["hasNextPage"] is False

    @pytest.mark.asyncio
    async def test_employees_connection_with_cursor(self, sample_data, execute_query):
        # First get the first page
        first_query = """
            query {
                employeesConnection(first: 1) {
                    edges {
                        cursor
                        node {
                            name
                        }
                    }
                    pageInfo {
                        endCursor
                    }
                }
            }
        """
        first_result = await execute_query(first_query)

        assert first_result.errors is None
        end_cursor = first_result.data["employeesConnection"]["pageInfo"]["endCursor"]

        # Now get the next page using the cursor
        second_query = f"""
            query {{
                employeesConnection(first: 2, after: "{end_cursor}") {{
                    edges {{
                        node {{
                            name
                        }}
                    }}
                }}
            }}
        """
        second_result = await execute_query(second_query)

        assert second_result.errors is None
        second_edges = second_result.data["employeesConnection"]["edges"]
        assert len(second_edges) == 2  # 3 total - 1 from first page = 2
