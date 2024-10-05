import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck_endpoint_returns_healthy_status(async_client: AsyncClient):
    """Test the /healthcheck endpoint.

    This test checks if the /healthcheck endpoint returns a status code of 200
    and a response body indicating that both the app and PostgreSQL are healthy.

    Args:
        async_client (AsyncClient): The HTTP client used to make the request.
    """
    response = await async_client.get("/healthcheck")
    assert response.status_code == 200

    response_body = response.json()
    assert response_body["app"] == "healthy"
    assert response_body["postgresql"] == "healthy"
