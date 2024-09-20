import os

import pytest
import pytest_asyncio

from src.core.settings import Settings


@pytest_asyncio.fixture(scope="function")
def set_postgres_db():
    original_value = os.environ.get("POSTGRES_URL")

    yield

    if original_value is not None:
        os.environ["POSTGRES_URL"] = original_value
    else:
        del os.environ["POSTGRES_URL"]


def test_postgres_url_assembly(set_postgres_db):
    expected_url = "postgresql+asyncpg://myuser:mypassword@localhost/mydatabase"
    os.environ["POSTGRES_URL"] = expected_url

    settings = Settings()
    assert settings.POSTGRES_URL == expected_url


def test_env_variables():
    required_env_variables = [
        "SECRET_KEY",
        "POSTGRES_USER",
        "POSTGRES_HOST",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
    ]

    missing_env_variables: list[str] = []
    for var in required_env_variables:
        if not os.getenv(var):
            missing_env_variables.append(var)

    if not missing_env_variables:
        return

    missing_env_variables_str = ", ".join(missing_env_variables)
    pytest.fail(f"Required environment variables are missing: {missing_env_variables_str}")
