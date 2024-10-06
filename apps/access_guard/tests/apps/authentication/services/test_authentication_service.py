import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.users import user_login
from src.apps.users.models import User
from src.apps.users.schemas import CreateUserData
from src.apps.users.services import create_user, get_current_user


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_user_login_valid_credentials(
        self,
        async_db_session: AsyncSession,
        authorize: AuthJwt,
        user_data: CreateUserData,
    ):
        """Test user login with valid credentials.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            authorize (AuthJwt): The authorization JWT object.
            user_data (CreateUserData): The data of the user to be created.

        Asserts:
            jwt_payload (BaseModel): The JWT payload should be an instance of BaseModel.
            jwt_payload.access_token (str): The access token should be a string.
        """
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
        authorize: AuthJwt,
        created_user: User,
    ):
        """Test user login with invalid credentials.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            authorize (AuthJwt): The authorization JWT object.
            created_user (User): The created user instance.

        Asserts:
            exc_info.value.status_code (int): The status code should be 401.
            exc_info.value.detail (str): The detail message should be "Invalid username or password".
        """
        auth_data = OAuth2PasswordRequestForm(
            username=created_user.username,
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
        authorize: AuthJwt,
        user_data: CreateUserData,
    ):
        """Test getting session data after user login.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            authorize (AuthJwt): The authorization JWT object.
            user_data (CreateUserData): The data of the user to be created.

        Asserts:
            user (BaseModel): The created user should be an instance of BaseModel.
        """
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
        authorize: AuthJwt,
    ):
        """Test invalid session data.

        Args:
            async_db_session (AsyncSession): The asynchronous database session.
            authorize (AuthJwt): The authorization JWT object.
        """
        access_token = authorize.create_access_token(subject=0)

        with pytest.raises(HTTPException):
            await get_current_user(
                access_token=access_token,
                db=async_db_session,
                authorize=authorize,
            )
