import pytest
from httpx import codes

from src.core.auth_handler import encode_token
from src.core.schemas.auth import CreateUser
from src.services.users import create_user


@pytest.fixture
def user_data():
    return CreateUser(
        name="Elliot Alderson 4",
        username="Mr_r0b0t",
        password="p4ain_",
    )


@pytest.mark.asyncio
async def test_user_register(client, user_data):
    response = await client.post(
        url="/auth/register",
        json=user_data.model_dump(),
    )
    assert response.status_code == codes.CREATED.value

    response_payload = response.json()
    assert response_payload["name"] == user_data.name
    assert response_payload["username"] == user_data.username


@pytest.mark.asyncio
async def test_user_login(client, async_db_session, user_data):
    await create_user(db=async_db_session, user_data=user_data)

    response = await client.post(
        url="/auth/token",
        data={"username": user_data.username, "password": user_data.password},
    )

    assert response.status_code == codes.OK.value

    response_payload = response.json()
    assert "access_token" in response_payload
    assert "refresh_token" in response_payload
    assert isinstance(response_payload["access_token"], str)
    assert isinstance(response_payload["refresh_token"], str)


@pytest.mark.asyncio
async def test_user_me(client, async_db_session, user_data):
    user = await create_user(db=async_db_session, user_data=user_data)

    auth_token_reponse = await client.post(
        url="/auth/token",
        data={"username": user_data.username, "password": user_data.password},
    )
    auth_token_reponse_payload = auth_token_reponse.json()

    user_me_repsonse = await client.post(
        url="/auth/me",
        json={"access_token": auth_token_reponse_payload["access_token"]},
    )
    assert user_me_repsonse.status_code == codes.OK.value

    user_me_repsonse_payload = user_me_repsonse.json()

    assert user.name == user_me_repsonse_payload["name"]
    assert user.username == user_me_repsonse_payload["username"]


@pytest.mark.asyncio
async def test_invalid_user_me(client, async_db_session, user_data):
    access_token = encode_token(user_id=0)

    user_me_repsonse = await client.post(
        url="/auth/me",
        json={"access_token": access_token},
    )
    assert user_me_repsonse.status_code == codes.UNAUTHORIZED.value

    user_me_repsonse_payload = user_me_repsonse.json()
    assert user_me_repsonse_payload["detail"] == "Token not associated with any user"
