import pytest
from sqlalchemy import text

from src.core.database import get_db


@pytest.mark.asyncio
async def test_get_database():
    async for db in get_db():
        result = await db.execute(text("SELECT 1"))
        assert result.scalars().first() == 1
