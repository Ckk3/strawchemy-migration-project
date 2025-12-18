import pytest
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader

from database import Base
from models import Department, Employee


@pytest.fixture(scope="function")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def mock_get_session(session, mocker: MockerFixture):
    """Automatically mock get_session to use the test session for all tests."""
    mocker.patch("schema.get_session", return_value=session)


@pytest.fixture
def graphql_context(session):
    return {
        "sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session),
    }


@pytest.fixture
def sample_data(session):
    engineering = Department(name="Engineering")
    marketing = Department(name="Marketing")
    session.add_all([engineering, marketing])
    session.flush()

    employees = [
        Employee(
            name="Alice Johnson",
            email="alice@example.com",
            password_hash="hashed_password_1",
            department_id=engineering.id,
        ),
        Employee(
            name="Bob Smith",
            email="bob@example.com",
            password_hash="hashed_password_2",
            department_id=engineering.id,
        ),
        Employee(
            name="Carol Williams",
            email="carol@example.com",
            password_hash="hashed_password_3",
            department_id=marketing.id,
        ),
    ]
    session.add_all(employees)
    session.commit()

    return {
        "departments": [engineering, marketing],
        "employees": employees,
    }
