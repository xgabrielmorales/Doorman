import os

import pytest

from src.core.settings import Settings


@pytest.mark.asyncio
def test_postgres_url_assembly(set_postgres_db):
    expected_url = "postgresql+asyncpg://myuser:mypassword@localhost/mydatabase"
    os.environ["POSTGRES_URL"] = expected_url

    settings = Settings()
    assert settings.POSTGRES_URL == expected_url


@pytest.mark.asyncio
def test_env_variables():
    required_env_variables = [
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
