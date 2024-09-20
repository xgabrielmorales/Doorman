from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from freezegun import freeze_time
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.future import select

from src.core.auth_handler import ALGORITHM, encode_token
from src.core.models.user import User
from src.core.schemas.auth import CreateUser
from src.core.settings import settings
from src.services.users import create_user, get_current_user, user_login


@pytest.fixture
def user_data():
    return CreateUser(
        name="Test User",
        username="testuser",
        password="password123",
    )


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_user_new_username(self, async_db_session, user_data):
        user = await create_user(db=async_db_session, user_data=user_data)

        query = select(User).where(User.username == user_data.username)
        result = await async_db_session.execute(query)
        created_user = result.scalars().first()

        assert user.username == user_data.username
        assert user.name == user_data.name

        assert created_user is not None

    @pytest.mark.asyncio
    async def test_create_user_existing_username(self, async_db_session, user_data):
        await create_user(db=async_db_session, user_data=user_data)

        with pytest.raises(HTTPException) as exc_info:
            await create_user(db=async_db_session, user_data=user_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "User with the same username or document number already exists" in str(
            exc_info.value,
        )

    @pytest.mark.asyncio
    async def test_create_user_password_hashing(self, async_db_session, user_data):
        user = await create_user(db=async_db_session, user_data=user_data)

        assert user.password != user_data.password


class TestUserLogin:
    @pytest.mark.asyncio
    async def test_user_login_valid_credentials(self, async_db_session, user_data):
        await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password=user_data.password,
        )

        jwt_payload = await user_login(async_db_session, auth_data)

        assert isinstance(jwt_payload, BaseModel)
        assert isinstance(jwt_payload.access_token, str)

    @pytest.mark.asyncio
    async def test_user_login_invalid_credentials(self, async_db_session, user_data):
        await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password="Wrong password",
        )

        with pytest.raises(HTTPException) as exc_info:
            await user_login(db=async_db_session, auth_data=auth_data)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid username or password"

    @pytest.mark.asyncio
    async def test_user_get_session_data(self, async_db_session, user_data):
        user = await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password=user_data.password,
        )

        jwt_payload = await user_login(async_db_session, auth_data)

        authenticated_user = await get_current_user(
            access_token=jwt_payload.access_token,
            db=async_db_session,
        )

        assert user.id == authenticated_user.id
        assert user.username == authenticated_user.username


class TestJWT:
    @pytest.mark.asyncio
    async def test_invalid_token(self, async_db_session, user_data):
        invalid_access_token = "eyJhbGciOiJIpXVCJ9.eyJzdWjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwV_adQssw5c"

        with pytest.raises(HTTPException, match="401: Invalid token"):
            await get_current_user(access_token=invalid_access_token, db=async_db_session)

    @pytest.mark.asyncio
    async def test_expired_token(self, async_db_session, user_data):
        await create_user(db=async_db_session, user_data=user_data)

        auth_data = OAuth2PasswordRequestForm(
            username=user_data.username,
            password=user_data.password,
        )

        jwt_payload = await user_login(async_db_session, auth_data)
        PLUS_30_MINUTES = datetime.now() + timedelta(minutes=30, seconds=1)

        with freeze_time(PLUS_30_MINUTES), pytest.raises(
            HTTPException,
            match="401: Signature has expired",
        ):
            await get_current_user(access_token=jwt_payload.access_token, db=async_db_session)

    @pytest.mark.asyncio
    async def test_modified_token(self, async_db_session, user_data):
        modified_access_token = jwt.encode(
            claims={"random": "key"},
            key=settings.SECRET_KEY,
            algorithm=ALGORITHM,
        )

        with pytest.raises(HTTPException, match="401: Invalid token payload"):
            await get_current_user(access_token=modified_access_token, db=async_db_session)

    @pytest.mark.asyncio
    async def test_access_token_non_existing_user(self, async_db_session, user_data):
        access_token = encode_token(user_id=0)

        with pytest.raises(HTTPException, match="401: Token not associated with any user"):
            await get_current_user(access_token=access_token, db=async_db_session)
