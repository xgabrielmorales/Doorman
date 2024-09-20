import os

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.core.database import get_db
from src.core.settings import settings
from src.main import app

async_engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=True,
    poolclass=NullPool,
)

TestingAsyncSessionLocal = sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)


@pytest_asyncio.fixture(scope="function")
async def async_db_session():
    connection = await async_engine.connect()
    trans = await connection.begin()
    async_session = TestingAsyncSessionLocal(bind=connection)

    try:
        yield async_session
    finally:
        await trans.rollback()
        await async_session.close()
        await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(async_db_session) -> TestClient:
    app.dependency_overrides[get_db] = lambda: async_db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
def set_postgres_db():
    original_value = os.environ.get("POSTGRES_URL")

    yield

    if original_value is not None:
        os.environ["POSTGRES_URL"] = original_value
    else:
        del os.environ["POSTGRES_URL"]
