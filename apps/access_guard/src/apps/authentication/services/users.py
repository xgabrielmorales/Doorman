from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import AuthGrantedData
from src.apps.authentication.services.jwt import AuthJwt
from src.apps.users.models import User
from src.core.password import verify_password


async def user_login(
    db: AsyncSession,
    auth_data: OAuth2PasswordRequestForm,
    authorize: AuthJwt,
) -> AuthGrantedData:
    query = select(User).where(User.username == auth_data.username)
    result = await db.exec(query)
    user = result.first()

    if user is None or not verify_password(auth_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = authorize.create_access_token(subject=user.id)
    refresh_token = authorize.create_refresh_token(subject=user.id)

    return AuthGrantedData(
        access_token=access_token,
        refresh_token=refresh_token,
    )
