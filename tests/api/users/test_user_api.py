import pytest
from httpx import codes

from src.apps.authentication.schemas import CreateUserData
from src.apps.authentication.services import create_user, encode_token


@pytest.fixture
def user_data():
    return CreateUserData(
        name="Elliot Alderson 4",
        username="Mr_r0b0t",
        password="p4ain_",
    )


@pytest.mark.asyncio
async def test_user_me(async_client, async_db_session, user_data):
    user = await create_user(db=async_db_session, user_data=user_data)

    auth_token_reponse = await async_client.post(
        url="/auth/login",
        data={"username": user_data.username, "password": user_data.password},
    )
    auth_token_reponse_payload = auth_token_reponse.json()

    user_me_repsonse = await async_client.post(
        url="/users/me",
        json={"access_token": auth_token_reponse_payload["access_token"]},
    )
    assert user_me_repsonse.status_code == codes.OK.value

    user_me_repsonse_payload = user_me_repsonse.json()

    assert user.name == user_me_repsonse_payload["name"]
    assert user.username == user_me_repsonse_payload["username"]


@pytest.mark.asyncio
async def test_invalid_user_me(async_client, async_db_session, user_data):
    access_token = encode_token(user_id=0)

    user_me_repsonse = await async_client.post(
        url="/users/me",
        json={"access_token": access_token},
    )
    assert user_me_repsonse.status_code == codes.UNAUTHORIZED.value

    user_me_repsonse_payload = user_me_repsonse.json()
    assert user_me_repsonse_payload["detail"] == "Token not associated with any user"
