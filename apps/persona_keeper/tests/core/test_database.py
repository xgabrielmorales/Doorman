import pytest
from sqlalchemy import select

from src.core.database import get_db


@pytest.mark.asyncio
async def test_get_database():
    async for db in get_db():
        result = await db.exec(select(1))
        assert result.scalars().first() == 1
