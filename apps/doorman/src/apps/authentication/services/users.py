from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import AuthGrantedData, CreateUserData
from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.password import hash_password, verify_password
from src.apps.users.models import User


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
