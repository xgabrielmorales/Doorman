import os

from src.core.settings import Settings


def test_postgres_url_assembly(set_postgres_db):
    expected_url = "postgresql+asyncpg://myuser:mypassword@localhost/mydatabase"
    os.environ["POSTGRES_URL"] = expected_url

    settings = Settings()
    assert settings.POSTGRES_URL == expected_url
