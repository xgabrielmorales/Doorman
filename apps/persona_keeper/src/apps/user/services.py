from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.auth.jwt import AuthJWT
from src.apps.auth.schemas import oauth2_scheme
from src.apps.user.models import User
from src.apps.user.schemas import CreateUserData
from src.core.database import get_db
from src.core.password import hash_password


async def create_user(
    db: AsyncSession,
    user_data: CreateUserData,
) -> User:
    query = select(User).where(User.username == user_data.username)
    result = await db.exec(query)

    user: User | None = result.first()

    if user:
        detail = "User with the same username already exists"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    db_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        password=hash_password(user_data.password),
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
    authorize: Annotated[AuthJWT, Depends()],
) -> User:
    token = authorize.decode_token(encoded_token=access_token)

    query = select(User).where(User.id == int(token.sub))
    result = await db.exec(query)
    user: User | None = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not associated with any user",
        )

    return user
