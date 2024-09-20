from datetime import UTC, datetime, timedelta

import pydantic
from fastapi import HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.core.schemas.auth import EncodedTokenData
from src.core.settings import settings

ALGORITHM = "HS256"

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def encode_token(user_id: int) -> str:
    utc_now = datetime.now(UTC)

    payload: EncodedTokenData = EncodedTokenData(
        exp=(utc_now + timedelta(minutes=30)),
        iat=utc_now,
        sub=str(user_id),
    )

    return jwt.encode(
        claims=payload.model_dump(),
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(access_token: str) -> EncodedTokenData:
    try:
        raw_payload: dict = jwt.decode(
            token=access_token,
            key=settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        detail = "Signature has expired"
        raise HTTPException(status_code=401, detail=detail)
    except jwt.JWTError:
        detail = "Invalid token"
        raise HTTPException(status_code=401, detail=detail)

    try:
        payload = EncodedTokenData(**raw_payload)
    except pydantic.ValidationError:
        detail = "Invalid token payload"
        raise HTTPException(status_code=401, detail=detail)

    return payload
