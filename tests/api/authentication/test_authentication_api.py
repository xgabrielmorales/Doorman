import pytest
from httpx import AsyncClient, codes
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import CreateUserData
from src.apps.authentication.services.users import create_user


@pytest.fixture
def user_data():
    return CreateUserData(
        first_name="Elliot",
        last_name=" Alderson 4",
        username="Mr_r0b0t",
        password="p4ain_",
    )


@pytest.mark.asyncio
async def test_user_register(
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
async def test_user_login(
    async_client: AsyncClient,
    async_db_session: AsyncSession,
    user_data: CreateUserData,
):
    await create_user(db=async_db_session, user_data=user_data)

    response = await async_client.post(
        url="/auth/login",
        data={"username": user_data.username, "password": user_data.password},
    )

    assert response.status_code == codes.OK.value

    response_payload = response.json()
    assert "access_token" in response_payload
    assert "refresh_token" in response_payload
    assert isinstance(response_payload["access_token"], str)
    assert isinstance(response_payload["refresh_token"], str)
