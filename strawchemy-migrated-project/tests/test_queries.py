from schema import schema


class TestEmployeesQuery:
    def test_employees_empty_database(self, graphql_context):
        query = """
        {
            employees {
                id
                name
                email
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None
        assert result.data["employees"] == []

    def test_employees_returns_all(self, sample_data, graphql_context):
        query = """
        {
            employees {
                id
                name
                email
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None
        assert len(result.data["employees"]) == 3

        names = [e["name"] for e in result.data["employees"]]
        emails = [e["email"] for e in result.data["employees"]]
        assert "Alice Johnson" in names
        assert "alice@example.com" in emails
        assert "Bob Smith" in names
        assert "bob@example.com" in emails
        assert "Carol Williams" in names
        assert "carol@example.com" in emails

    def test_employees_does_not_return_password_hash(
        self, sample_data, graphql_context
    ):
        query = """
        {
            employees {
                id
                name
                passwordHash
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is not None


class TestDepartmentsQuery:
    def test_departments_empty_database(self, graphql_context):
        query = """
        {
            departments {
                id
                name
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None
        assert result.data["departments"] == []

    def test_departments_returns_all(self, sample_data, graphql_context):
        query = """
        {
            departments {
                id
                name
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None
        assert len(result.data["departments"]) == 2

        names = [d["name"] for d in result.data["departments"]]
        assert "Engineering" in names
        assert "Marketing" in names


class TestNestedQueries:
    """Strawchemy uses simple lists instead of Relay-style pagination."""

    def test_employees_with_department(self, sample_data, graphql_context):
        query = """
        {
            employees {
                name
                department {
                    name
                }
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None

        employees_by_name = {e["name"]: e for e in result.data["employees"]}

        alice = employees_by_name["Alice Johnson"]
        assert alice["department"]["name"] == "Engineering"

        carol = employees_by_name["Carol Williams"]
        assert carol["department"]["name"] == "Marketing"

    def test_departments_with_employees(self, sample_data, graphql_context):
        query = """
        {
            departments {
                name
                employees {
                    name
                    email
                }
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None

        departments_by_name = {d["name"]: d for d in result.data["departments"]}

        engineering = departments_by_name["Engineering"]
        eng_employee_names = [e["name"] for e in engineering["employees"]]
        assert "Alice Johnson" in eng_employee_names
        assert "Bob Smith" in eng_employee_names
        assert len(eng_employee_names) == 2

        marketing = departments_by_name["Marketing"]
        mkt_employee_names = [e["name"] for e in marketing["employees"]]
        assert "Carol Williams" in mkt_employee_names
        assert len(mkt_employee_names) == 1

    def test_deeply_nested_query(self, sample_data, graphql_context):
        query = """
        {
            departments {
                name
                employees {
                    name
                    department {
                        name
                    }
                }
            }
        }
        """
        result = schema.execute_sync(query, context_value=graphql_context)

        assert result.errors is None

        departments_by_name = {d["name"]: d for d in result.data["departments"]}
        engineering = departments_by_name["Engineering"]
        first_employee = engineering["employees"][0]

        assert first_employee["department"]["name"] == "Engineering"
