import random
import string

import pytest
from httpx import AsyncClient, codes
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import CreateUserData
from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.users import create_user


@pytest.fixture
def user_data():
    return CreateUserData(
        first_name="Elliot",
        last_name=" Alderson 4",
        username="Mr_r0b0t",
        password="p4ain_",
    )


def random_word(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class TestAutorizationAPI:
    @pytest.mark.asyncio
    async def test_register(
        self,
        async_client: AsyncClient,
        user_data: CreateUserData,
    ):
        response = await async_client.post(
            url="/auth/register",
            json=user_data.model_dump(),
        )
        assert response.status_code == codes.CREATED.value

        response_payload = response.json()
        assert response_payload["first_name"] == user_data.first_name
        assert response_payload["last_name"] == user_data.last_name
        assert response_payload["username"] == user_data.username

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        argnames="valid_username, valid_password",
        argvalues=[(True, True), (True, False), (False, True), (False, False)],
    )
    async def test_login(
        self,
        async_client: AsyncClient,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        valid_username: bool,
        valid_password: bool,
    ):
        await create_user(db=async_db_session, user_data=user_data)

        data: dict[str, str] = {
            "username": user_data.username,
            "password": user_data.password,
        }

        if not valid_username:
            data["username"] = random_word(10)
        if not valid_password:
            data["password"] = random_word(10)

        response = await async_client.post(url="/auth/login", data=data)

        if valid_username and valid_password:
            assert response.status_code == codes.OK.value
            response_payload = response.json()
            assert isinstance(response_payload["access_token"], str)
            assert isinstance(response_payload["refresh_token"], str)
        else:
            assert response.status_code == codes.UNAUTHORIZED.value
            response_payload = response.json()
            assert response_payload["detail"] == "Invalid username or password"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        argnames="valid_refresh_token",
        argvalues=[True, False],
    )
    async def test_refresh_session(
        self,
        async_client: AsyncClient,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        authorize: AuthJwt,
        valid_refresh_token: bool,
    ):
        user = await create_user(db=async_db_session, user_data=user_data)

        refresh_token = authorize.create_refresh_token(subject=user.id)

        if not valid_refresh_token:
            refresh_token = refresh_token[::-1]

        response = await async_client.post(
            url="/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        if valid_refresh_token:
            assert response.status_code == codes.OK.value
            response_payload = response.json()
            assert isinstance(response_payload["access_token"], str)
            assert isinstance(response_payload["refresh_token"], str)
        else:
            assert response.status_code == codes.UNPROCESSABLE_ENTITY.value

    @pytest.mark.asyncio
    async def test_invalid_access_token_format(
        self,
        async_client: AsyncClient,
        async_db_session: AsyncSession,
        user_data: CreateUserData,
        authorize: AuthJwt,
    ):
        user = await create_user(db=async_db_session, user_data=user_data)

        token = authorize.create_access_token(subject=user.id)
        response = await async_client.post(
            url="/auth/refresh",
            headers={"Authorization": f"{token}"},
        )

        assert response.status_code == codes.UNPROCESSABLE_ENTITY.value

        response_payload = response.json()
        assert (
            response_payload["detail"] == "Bad Authorization header. Expected value 'Bearer <JWT>'"
        )
