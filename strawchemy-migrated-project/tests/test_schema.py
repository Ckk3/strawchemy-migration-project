from schema import schema


class TestSchemaTypes:
    def test_schema_has_query_type(self):
        query_type = schema.query
        assert query_type is not None

    def test_query_has_employees_field(self):
        query_type = schema.query
        field_names = [
            field.name for field in query_type.__strawberry_definition__.fields
        ]
        assert "employees" in field_names

    def test_query_has_departments_field(self):
        query_type = schema.query
        field_names = [
            field.name for field in query_type.__strawberry_definition__.fields
        ]
        assert "departments" in field_names


class TestEmployeeType:
    def test_employee_type_has_expected_fields(self):
        query = """
        {
            __type(name: "EmployeeType") {
                fields {
                    name
                }
            }
        }
        """
        result = schema.execute_sync(query)
        assert result.errors is None

        field_names = [f["name"] for f in result.data["__type"]["fields"]]

        assert "id" in field_names
        assert "name" in field_names
        assert "email" in field_names
        assert "department" in field_names

    def test_password_hash_is_excluded(self):
        query = """
        {
            __type(name: "EmployeeType") {
                fields {
                    name
                }
            }
        }
        """
        result = schema.execute_sync(query)
        assert result.errors is None

        field_names = [f["name"] for f in result.data["__type"]["fields"]]

        assert "password_hash" not in field_names
        assert "passwordHash" not in field_names


class TestDepartmentType:
    def test_department_type_has_expected_fields(self):
        query = """
        {
            __type(name: "DepartmentType") {
                fields {
                    name
                }
            }
        }
        """
        result = schema.execute_sync(query)
        assert result.errors is None

        field_names = [f["name"] for f in result.data["__type"]["fields"]]

        assert "id" in field_names
        assert "name" in field_names
        assert "employees" in field_names


class TestSchemaIntrospection:
    def test_introspect_employee_type_fields(self):
        query = """
        {
            __type(name: "EmployeeType") {
                name
                fields {
                    name
                }
            }
        }
        """
        result = schema.execute_sync(query)

        assert result.errors is None
        assert result.data["__type"]["name"] == "EmployeeType"

        field_names = [f["name"] for f in result.data["__type"]["fields"]]
        assert "id" in field_names
        assert "name" in field_names
        assert "email" in field_names
        assert "passwordHash" not in field_names
        assert "password_hash" not in field_names

    def test_introspect_department_type_fields(self):
        query = """
        {
            __type(name: "DepartmentType") {
                name
                fields {
                    name
                }
            }
        }
        """
        result = schema.execute_sync(query)

        assert result.errors is None
        assert result.data["__type"]["name"] == "DepartmentType"

        field_names = [f["name"] for f in result.data["__type"]["fields"]]
        assert "id" in field_names
        assert "name" in field_names
        assert "employees" in field_names
