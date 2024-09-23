import pytest
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import CreateUserData
from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.users import create_user, user_login
from src.apps.users.models import User
from src.apps.users.services import get_current_user


@pytest.fixture
def user_data():
    return CreateUserData(
        first_name="Test",
        last_name="User",
        username="testuser",
        password="password123",
    )


class TestUserRegistration:
    @pytest.mark.asyncio
    async def test_create_user_new_username(
        self,
        async_db_session: AsyncSession,
        user_data,
    ):
        user = await create_user(db=async_db_session, user_data=user_data)

        query = select(User).where(User.username == user_data.username)
        result = await async_db_session.execute(query)
        created_user = result.scalars().first()

        assert user.username == user_data.username
        assert user.first_name == user_data.first_name
        assert user.last_name == user_data.last_name

        assert created_user is not None

    @pytest.mark.asyncio
    async def test_create_user_existing_username(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
    ):
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
        user_data: CreateUserData,
    ):
        user = await create_user(db=async_db_session, user_data=user_data)

        assert user.password != user_data.password


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_user_login_valid_credentials(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        authorize: AuthJwt,
    ):
        await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password=user_data.password,
        )

        jwt_payload = await user_login(
            db=async_db_session,
            auth_data=auth_data,
            authorize=authorize,
        )

        assert isinstance(jwt_payload, BaseModel)
        assert isinstance(jwt_payload.access_token, str)

    @pytest.mark.asyncio
    async def test_user_login_invalid_credentials(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        authorize: AuthJwt,
    ):
        await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password="Wrong password",
        )

        with pytest.raises(HTTPException) as exc_info:
            await user_login(
                db=async_db_session,
                auth_data=auth_data,
                authorize=authorize,
            )

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid username or password"

    @pytest.mark.asyncio
    async def test_get_session_data(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        authorize: AuthJwt,
    ):
        user = await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password=user_data.password,
        )

        jwt_payload = await user_login(
            db=async_db_session,
            auth_data=auth_data,
            authorize=authorize,
        )

        authenticated_user = await get_current_user(
            access_token=jwt_payload.access_token,
            db=async_db_session,
            authorize=authorize,
        )

        assert user.id == authenticated_user.id
        assert user.username == authenticated_user.username

    @pytest.mark.asyncio
    async def test_invalid_session_data(
        self,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        authorize: AuthJwt,
    ):
        access_token = authorize.create_access_token(subject=0)

        with pytest.raises(HTTPException):
            await get_current_user(
                access_token=access_token,
                db=async_db_session,
                authorize=authorize,
            )
