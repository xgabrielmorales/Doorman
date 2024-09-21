from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
import pydantic
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import AuthGrantedData, CreateUserData, EncodedTokenData
from src.apps.users.models import User
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
        payload=payload.model_dump(),
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(access_token: str) -> EncodedTokenData:
    try:
        raw_payload: dict = jwt.decode(
            jwt=access_token,
            key=settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        detail = "Signature has expired"
        raise HTTPException(status_code=401, detail=detail)
    except jwt.PyJWTError:
        detail = "Invalid token"
        raise HTTPException(status_code=401, detail=detail)

    try:
        payload = EncodedTokenData(**raw_payload)
    except pydantic.ValidationError:
        detail = "Invalid token payload"
        raise HTTPException(status_code=401, detail=detail)

    return payload


async def create_user(
    db: AsyncSession,
    user_data: CreateUserData,
) -> User:
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)

    user: User | None = result.scalars().first()

    if user:
        detail = "User with the same username already exists"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    db_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        password=get_password_hash(user_data.password),
    )

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def user_login(
    db: AsyncSession,
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthGrantedData:
    query = select(User).where(User.username == auth_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None or not verify_password(auth_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = encode_token(user_id=user.id)

    return AuthGrantedData(
        access_token=access_token,
        refresh_token="",
    )
