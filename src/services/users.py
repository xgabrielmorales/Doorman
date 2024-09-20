from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.core.auth_handler import encode_token, get_password_hash, verify_password
from src.core.models.user import User
from src.core.schemas.auth import AuthGrantedData, CreateUser


async def create_user(
    db: Session,
    user_data: CreateUser,
) -> User:
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)

    result = result.scalars().first()

    if result:
        detail = "User with the same username or document number already exists"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    db_user = User(
        name=user_data.name,
        username=user_data.username,
        password=get_password_hash(user_data.password),
    )

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def user_login(
    db: Session,
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
