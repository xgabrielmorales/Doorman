from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.services.jwt import AuthJwt, oauth2_scheme
from src.apps.users.models import User
from src.core.database import get_db


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
    authorize: Annotated[AuthJwt, Depends()],
) -> User:
    token = authorize.get_jwt(encoded_token=access_token)

    query = select(User).where(User.id == int(token.sub))
    result = await db.exec(query)
    user: User | None = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not associated with any user",
        )

    return user
