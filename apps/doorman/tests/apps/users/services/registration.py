import pytest
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.users.models import User
from src.apps.users.services import create_user
from tests.apps.users.factories import CreateUserDataFactory


class TestUserRegistration:
    @pytest.mark.asyncio
    async def test_create_user_new_username(
        self,
        async_db_session: AsyncSession,
    ):
        user_data = CreateUserDataFactory.build()
        user = await create_user(db=async_db_session, user_data=user_data)

        query = select(User).where(User.username == user_data.username)
        result = await async_db_session.exec(query)
        created_user = result.first()

        assert user.username == user_data.username
        assert user.first_name == user_data.first_name
        assert user.last_name == user_data.last_name

        assert created_user is not None

    @pytest.mark.asyncio
    async def test_create_user_existing_username(
        self,
        async_db_session: AsyncSession,
    ):
        user_data = CreateUserDataFactory.build()
        await create_user(db=async_db_session, user_data=user_data)

        with pytest.raises(HTTPException) as exc_info:
            await create_user(db=async_db_session, user_data=user_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "User with the same username already exists" in str(
            exc_info.value,
        )

    @pytest.mark.asyncio
    async def test_create_user_password_hashing(
        self,
        async_db_session: AsyncSession,
    ):
        user_data = CreateUserDataFactory.build()
        user = await create_user(db=async_db_session, user_data=user_data)

        assert user.password != user_data.password
