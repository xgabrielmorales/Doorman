from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.authentication.schemas import (
    AuthGrantedData,
    CreatedUserData,
    CreateUserData,
)
from src.apps.authentication.services.jwt import AuthJwt
from src.apps.authentication.services.users import create_user, user_login
from src.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: CreateUserData,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CreatedUserData:
    user = await create_user(db=db, user_data=user_data)

    return CreatedUserData.model_validate(user)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorize: Annotated[AuthJwt, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthGrantedData:
    return await user_login(db=db, authorize=authorize, auth_data=auth_data)


@router.post("/refresh")
def refresh(
    authorize: AuthJwt = Depends(),
) -> AuthGrantedData:
    authorize.jwt_refresh_token_required()

    token = authorize.get_jwt()

    access_token = authorize.create_access_token(subject=token.sub)
    refresh_token = authorize.create_refresh_token(subject=token.sub)

    return AuthGrantedData(access_token=access_token, refresh_token=refresh_token)
