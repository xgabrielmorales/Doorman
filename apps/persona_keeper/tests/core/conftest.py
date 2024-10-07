import os

import pytest_asyncio


@pytest_asyncio.fixture(scope="function")
def set_postgres_db():
    original_value = os.environ.get("POSTGRES_URL")

    yield

    if original_value is not None:
        os.environ["POSTGRES_URL"] = original_value
    else:
        del os.environ["POSTGRES_URL"]
