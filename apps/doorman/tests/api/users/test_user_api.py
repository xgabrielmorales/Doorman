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
        last_name="Alderson",
        username="Mr_r0b0t",
        password="p4ain_",
    )


@pytest.mark.asyncio
async def test_user_me(
    async_client: AsyncClient,
    async_db_session: AsyncSession,
    user_data: CreateUserData,
):
    user = await create_user(db=async_db_session, user_data=user_data)

    auth_token_reponse = await async_client.post(
        url="/auth/login",
        data={"username": user_data.username, "password": user_data.password},
    )
    auth_token_reponse_payload = auth_token_reponse.json()

    user_me_repsonse = await async_client.post(
        url="/users/me",
        headers={"Authorization": f"Bearer {auth_token_reponse_payload["access_token"]}"},
    )
    assert user_me_repsonse.status_code == codes.OK.value

    user_me_repsonse_payload = user_me_repsonse.json()

    assert user.first_name == user_me_repsonse_payload["first_name"]
    assert user.last_name == user_me_repsonse_payload["last_name"]
    assert user.username == user_me_repsonse_payload["username"]


@pytest.mark.asyncio
async def test_invalid_user_me(
    async_client: AsyncClient,
    async_db_session: AsyncSession,
    user_data: CreateUserData,
    authorize: AuthJwt,
):
    access_token = authorize.create_access_token(subject=0)

    user_me_repsonse = await async_client.post(
        url="/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert user_me_repsonse.status_code == codes.UNAUTHORIZED.value

    user_me_repsonse_payload = user_me_repsonse.json()
    assert user_me_repsonse_payload["detail"] == "Token not associated with any user"
