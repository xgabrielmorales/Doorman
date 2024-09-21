from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.apps.authentication.schemas import (
    AuthGrantedData,
    CreatedUserData,
    CreateUserData,
)
from src.apps.authentication.services import create_user, user_login
from src.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: CreateUserData,
    db: Session = Depends(get_db),
) -> CreatedUserData:
    return await create_user(db=db, user_data=user_data)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> AuthGrantedData:
    return await user_login(db=db, auth_data=auth_data)
