from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.services import decode_access_token, oauth2_scheme
from src.apps.users.models import User
from src.core.database import get_db


async def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
) -> User:
    jwt_payload = decode_access_token(access_token=access_token)

    user_id = jwt_payload.sub

    query = select(User).where(User.id == int(user_id))
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not associated with any user",
        )

    return user
