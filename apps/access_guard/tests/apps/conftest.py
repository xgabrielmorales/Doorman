import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.users.models import User
from src.apps.users.schemas import CreateUserData
from src.apps.users.services import create_user
from tests.apps.users.factories import CreateUserDataFactory


@pytest.fixture
def user_data() -> CreateUserData:
    return CreateUserDataFactory.build()


@pytest_asyncio.fixture(scope="function")
async def created_user(async_db_session: AsyncSession, user_data: CreateUserData) -> User:
    return await create_user(db=async_db_session, user_data=user_data)
