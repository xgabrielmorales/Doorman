import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.users import user_login
from src.apps.users.services import create_user, get_current_user
from tests.apps.users.factories import CreateUserDataFactory


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_user_login_valid_credentials(
        self,
        async_db_session: AsyncSession,
        authorize: AuthJwt,
    ):
        user_data = CreateUserDataFactory.build()
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
    ):
        user_data = CreateUserDataFactory.build()
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
        authorize: AuthJwt,
    ):
        user_data = CreateUserDataFactory.build()
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
        access_token = authorize.create_access_token(subject=0)

        with pytest.raises(HTTPException):
            await get_current_user(
                access_token=access_token,
                db=async_db_session,
                authorize=authorize,
            )
