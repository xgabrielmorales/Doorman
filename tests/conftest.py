import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

async_engine = create_async_engine(
    settings.POSTGRES_URL,
    pool_size=5,
    echo=True,
    max_overflow=10,
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
    nested = await connection.begin_nested()

    @event.listens_for(async_session.sync_session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.sync_connection.begin_nested()

    yield async_session

    await trans.rollback()
    await async_session.close()
    await connection.close()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()


@pytest.fixture(scope="session")
def client() -> TestClient:
    from src.main import app

    return TestClient(app)
