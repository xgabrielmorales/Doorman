from datetime import datetime, timedelta

import jwt
import pytest

from src.apps.authentication.schemas import Token
from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.jwt_exceptions import (
    AuthJwtDecodeError,
    InvalidHeaderError,
    AuthJwtRefreshTokenRequired,
    AuthJwtAccessTokenRequired,
)
from src.core.settings import settings
from unittest.mock import MagicMock


class TestAuthJWTService:
    @pytest.mark.asyncio
    def test_constructor(self):
        request = MagicMock()
        request.headers = {
            "authorization": "Bearer eyJhbGciOiIsIn9.eyJG4gRG9lINDIyfQ.Sfl36POk6yJV_adQssw5c",
        }

        autorize = AuthJwt(request=request)

        assert autorize._token == request.headers["authorization"].split()[1]

    @pytest.mark.asyncio
    def test_jwt_identifier(self, authorize: AuthJwt):
        assert isinstance(authorize._get_jwt_identifier(), str)

    @pytest.mark.asyncio
    def test_jwt_from_headers(self, authorize: AuthJwt):
        authorization_header = "Bearer eyJhbGciOiIsIn9.eyJG4gRG9lINDIyfQ.Sfl36POk6yJV_adQssw5c"
        authorize._get_jwt_from_headers(auth=authorization_header)
        assert authorize._token == authorization_header.split()[1]

    @pytest.mark.asyncio
    def test_invalid_jwt_from_headers(self, authorize: AuthJwt):
        with pytest.raises(InvalidHeaderError):
            authorize._get_jwt_from_headers(auth="random string")

    @pytest.mark.asyncio
    def test_int_from_datetime(self, authorize: AuthJwt):
        now = datetime.now()
        assert authorize._get_int_from_datetime(now) == int(now.timestamp())

    @pytest.mark.asyncio
    def test__invalid_int_from_datetime(self, authorize: AuthJwt):
        with pytest.raises(TypeError):
            authorize._get_int_from_datetime(None)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    def test_create_valid_type_tokens(self, authorize: AuthJwt):
        access_token = authorize.create_access_token(subject=1)
        refresh_token = authorize.create_refresh_token(subject=1)

        decoded_access_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        decoded_refresh_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

        assert decoded_access_token["type"] == "access"
        assert decoded_refresh_token["type"] == "refresh"

    @pytest.mark.asyncio
    def test_create_invalid_type_tokens(self, authorize: AuthJwt):
        with pytest.raises(TypeError):
            authorize.create_access_token(subject=None)  # type: ignore[arg-type]

        with pytest.raises(TypeError):
            authorize.create_refresh_token(subject=None)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    def test_create_valid_tokens(self, authorize: AuthJwt):
        exp_time = int((datetime.now() + timedelta(minutes=1)).timestamp())

        assert isinstance(authorize._create_token(1, "access"), str)
        assert isinstance(authorize._create_token(1, "refresh"), str)
        assert isinstance(authorize._create_token(1, "access", exp_time), str)
        assert isinstance(authorize._create_token(1, "refresh", exp_time), str)

    @pytest.mark.asyncio
    def test_create_invalid_tokens(self, authorize: AuthJwt):
        with pytest.raises(TypeError):
            authorize._create_token(subject=29.4, token_type="access")  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            authorize._create_token(subject=1, token_type="random")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            authorize._create_token(subject=1, token_type="access", exp_time=False)

    def test_get_valid_jwt(self, authorize: AuthJwt):
        access_token = authorize.create_access_token(subject=1)
        refresh_token = authorize.create_refresh_token(subject=1)

        assert isinstance(authorize.get_jwt(access_token), Token)
        assert isinstance(authorize.get_jwt(refresh_token), Token)

    def test_get_invalid_jwt(self, authorize: AuthJwt):
        with pytest.raises(AuthJwtDecodeError):
            authorize.get_jwt("random_string")

    def test_verify_jwt_in_request(self, authorize: AuthJwt):
        access_token = authorize.create_refresh_token(subject=1)

        with pytest.raises(ValueError):
            authorize._verify_jwt_in_request(access_token, "random_type")  # type: ignore[arg-type]

        access_token = authorize.create_access_token(subject=1)
        with pytest.raises(AuthJwtRefreshTokenRequired):
            authorize._verify_jwt_in_request(access_token, "refresh")

        refresh_token = authorize.create_refresh_token(subject=1)
        with pytest.raises(AuthJwtAccessTokenRequired):
            authorize._verify_jwt_in_request(refresh_token, "access")

    def test_valid_jwt_token_required(self, authorize: AuthJwt):
        access_token = authorize.create_refresh_token(subject=1)
        authorize._token = access_token

        assert authorize.jwt_refresh_token_required() is None

        access_token = authorize.create_access_token(subject=1)
        authorize._token = access_token

        assert authorize.jwt_access_token_required() is None

    def test_invalid_jwt_token_required(self, authorize: AuthJwt):
        access_token = authorize.create_access_token(subject=1)
        authorize._token = access_token
        with pytest.raises(AuthJwtRefreshTokenRequired):
            assert authorize.jwt_refresh_token_required()

        access_token = authorize.create_refresh_token(subject=1)
        authorize._token = access_token
        with pytest.raises(AuthJwtAccessTokenRequired):
            assert authorize.jwt_access_token_required()
