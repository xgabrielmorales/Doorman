import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from src.apps.authentication.schemas import Token
from src.apps.authentication.services.jwt_exceptions import (
    AuthJwtAccessTokenRequired,
    AuthJwtDecodeError,
    AuthJwtRefreshTokenRequired,
    InvalidHeaderError,
)
from src.core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthJwt:
    _access_token_expires = timedelta(minutes=15)
    _refresh_token_expires = timedelta(days=30)
    _algorithm = "HS256"
    _header_type = "Bearer"
    _header_name = "Authorization"
    _token: str | bytes | None = None

    def __init__(
        self,
        request: Request = None,  # type: ignore[assignment]
    ):
        if request:
            auth: str | None = request.headers.get(self._header_name.lower())

            if auth:
                self._get_jwt_from_headers(auth)

    def _get_jwt_from_headers(self, auth: str) -> None:
        header_name, header_type = self._header_name, self._header_type

        parts = auth.split()

        # <HeaderType> <JWT>
        # Example: Bearer eyJhbGciOiIsIn9.eyJG4gRG9lINDIyfQ.Sfl36POk6yJV_adQssw5c
        if not re.match(r"{}\s".format(header_type), auth) or len(parts) != 2:
            detail = f"Bad {header_name} header. Expected value '{header_type} <JWT>'"
            raise InvalidHeaderError(status_code=422, detail=detail)

        self._token = parts[1]

    def _get_jwt_identifier(self) -> str:
        return str(uuid.uuid4())

    def _get_int_from_datetime(self, value: datetime) -> int:
        if not isinstance(value, datetime):
            raise TypeError("a datetime is required")

        return int(value.timestamp())

    def _create_token(
        self,
        subject: str | int,
        token_type: Literal["access", "refresh"],
        exp_time: int | None = None,
    ) -> str:
        if type(subject) not in (str, int):
            raise TypeError("subject must be a String or Integer")

        if token_type not in ["access", "refresh"]:
            raise ValueError("token_type must be a String and must be either 'access' or 'refresh'")

        if exp_time is not None and type(exp_time) is not int:
            raise TypeError("exp_time must be an Integer or None")

        reserved_claims: dict[str, str | int] = {
            "iat": self._get_int_from_datetime(datetime.now(timezone.utc)),
            "sub": subject,
            "jti": self._get_jwt_identifier(),
        }
        custom_claims: dict[str, str | int] = {
            "type": token_type,
        }

        if exp_time:
            custom_claims["exp"] = exp_time

        token = Token.model_validate({**reserved_claims, **custom_claims})

        return jwt.encode(
            payload=token.model_dump(),
            key=settings.SECRET_KEY,
            algorithm=self._algorithm,
        )

    def create_access_token(self, subject: str | int) -> str:
        if not isinstance(subject, (str, int)):
            raise TypeError("subject must be a string or integer")

        now = datetime.now(timezone.utc)

        return self._create_token(
            subject=subject,
            token_type="access",
            exp_time=self._get_int_from_datetime(now + self._access_token_expires),
        )

    def create_refresh_token(self, subject: str | int) -> str:
        if not isinstance(subject, (str, int)):
            raise TypeError("subject must be a string or integer")

        now = datetime.now(timezone.utc)

        return self._create_token(
            subject=subject,
            token_type="refresh",
            exp_time=self._get_int_from_datetime(now + self._refresh_token_expires),
        )

    def get_jwt(self, encoded_token: str | bytes | None = None) -> Token:
        token = encoded_token or self._token
        algorithms = [self._algorithm]

        try:
            raw_jwt = jwt.decode(
                jwt=token,  # type: ignore[arg-type]
                key=settings.SECRET_KEY,
                algorithms=algorithms,
            )
        except Exception as err:
            raise AuthJwtDecodeError(status_code=422, detail=str(err))

        return Token(**raw_jwt)

    def _verify_jwt_in_request(
        self,
        token: str | bytes,
        token_type: Literal["access", "refresh"],
    ) -> None:
        if token_type not in ["access", "refresh"]:
            raise ValueError("token_type must be a string and must be either 'access' or 'refresh'")

        if self.get_jwt(token).type != token_type:
            detail = "Only {} tokens are allowed".format(token_type)
            if token_type == "access":
                raise AuthJwtAccessTokenRequired(status_code=422, detail=detail)
            if token_type == "refresh":
                raise AuthJwtRefreshTokenRequired(status_code=422, detail=detail)

    def jwt_refresh_token_required(self):
        self._verify_jwt_in_request(self._token, "refresh")  # type: ignore[arg-type]

    def jwt_access_token_required(self):
        self._verify_jwt_in_request(self._token, "access")  # type: ignore[arg-type]
