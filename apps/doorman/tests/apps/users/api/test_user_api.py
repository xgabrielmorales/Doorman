import pytest
from httpx import AsyncClient, codes
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.services.jwt import AuthJwt
from src.apps.users.services import create_user
from tests.apps.users.factories import CreateUserDataFactory


@pytest.mark.asyncio
async def test_user_me_endpoint_returns_user_info(
    async_client: AsyncClient,
    async_db_session: AsyncSession,
):
    """Test that the /users/me endpoint returns the authenticated user's information.

    Args:
        async_client (AsyncClient): The asynchronous HTTP client.
        async_db_session (AsyncSession): The asynchronous database session.
    """
    user_data = CreateUserDataFactory.build()
    created_user = await create_user(db=async_db_session, user_data=user_data)

    auth_token_response = await async_client.post(
        url="/auth/login",
        data={"username": user_data.username, "password": user_data.password},
    )
    auth_token_response_payload = auth_token_response.json()

    user_me_response = await async_client.post(
        url="/users/me",
        headers={"Authorization": f"Bearer {auth_token_response_payload['access_token']}"},
    )
    assert user_me_response.status_code == codes.OK.value

    user_me_response_payload = user_me_response.json()
    assert created_user.first_name == user_me_response_payload["first_name"]
    assert created_user.last_name == user_me_response_payload["last_name"]
    assert created_user.username == user_me_response_payload["username"]


@pytest.mark.asyncio
async def test_user_me_endpoint_with_invalid_token_returns_unauthorized(
    async_client: AsyncClient,
    async_db_session: AsyncSession,
    authorize: AuthJwt,
):
    """Test that the /users/me endpoint returns 401 Unauthorized for an invalid token.

    Args:
        async_client (AsyncClient): The asynchronous HTTP client.
        async_db_session (AsyncSession): The asynchronous database session.
        authorize (AuthJwt): The JWT authorization service.
    """
    access_token = authorize.create_access_token(subject=0)

    user_me_response = await async_client.post(
        url="/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert user_me_response.status_code == codes.UNAUTHORIZED.value

    user_me_response_payload = user_me_response.json()
    assert user_me_response_payload["detail"] == "Token not associated with any user"
