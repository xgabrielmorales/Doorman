import pytest
from httpx import AsyncClient, codes

from src.apps.user.schemas import CreateUserData
from tests.apps.user.factories import CreateUserDataFactory


class TestUserSignupAPI:
    @pytest.mark.asyncio
    async def test_register(
        self,
        async_client: AsyncClient,
    ):
        """Test registering a new user.

        Args:
            async_client (AsyncClient): The asynchronous HTTP client.
        """
        user_data = CreateUserDataFactory.build()
        response = await async_client.post(
            url="/users/register",
            json=user_data.model_dump(),
        )
        assert response.status_code == codes.CREATED.value

        response_payload = response.json()
        assert response_payload["first_name"] == user_data.first_name
        assert response_payload["last_name"] == user_data.last_name
        assert response_payload["username"] == user_data.username

    @pytest.mark.asyncio
    async def test_register_existing_user(
        self,
        async_client: AsyncClient,
        user_data: CreateUserData,
    ):
        """Test registering a user that already exists.

        Args:
            async_client (AsyncClient): The asynchronous HTTP client.
            user_data (CreateUserData): The user data for registration.
        """
        await async_client.post(
            url="/users/register",
            json=user_data.model_dump(),
        )

        response = await async_client.post(
            url="/users/register",
            json=user_data.model_dump(),
        )
        assert response.status_code == codes.BAD_REQUEST.value

        response_payload = response.json()
        assert response_payload["detail"] == "User with the same username already exists"
