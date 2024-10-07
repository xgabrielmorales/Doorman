import pytest
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.user.models import User
from src.apps.user.schemas import CreateUserData
from src.apps.user.services import create_user


class TestUserSignUp:
    @pytest.mark.asyncio
    async def test_create_user_with_new_username(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
    ):
        """Test that a user can be created with a new username.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            user_data (CreateUserData): The data of the user to be created.
        """
        await create_user(db=async_db_session, user_data=user_data)

        query = select(User).where(User.username == user_data.username)
        result = await async_db_session.exec(query)
        created_user = result.first()

        assert created_user is not None
        assert created_user.username == user_data.username
        assert created_user.first_name == user_data.first_name
        assert created_user.last_name == user_data.last_name

    @pytest.mark.asyncio
    async def test_create_user_with_existing_username_raises_exception(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
    ):
        """Test that creating a user with an existing username raises an exception.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            user_data (CreateUserData): The data of the user to be created.

        Raises:
            HTTPException: If the username already exists.
        """
        await create_user(db=async_db_session, user_data=user_data)

        with pytest.raises(HTTPException) as exc_info:
            await create_user(db=async_db_session, user_data=user_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "User with the same username already exists" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_user_password_is_hashed(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
    ):
        """Test that the user's password is stored as a hash.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            user_data (CreateUserData): The data of the user to be created.
        """
        await create_user(db=async_db_session, user_data=user_data)

        query = select(User).where(User.username == user_data.username)
        result = await async_db_session.exec(query)
        created_user = result.first()

        assert created_user is not None
        assert created_user.password != user_data.password
        assert len(created_user.password) > 0
