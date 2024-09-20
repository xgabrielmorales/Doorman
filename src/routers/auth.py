from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.schemas.auth import AuthGrantedData, CreatedUserData, CreateUser, UserMeRequestData
from src.services.users import create_user, get_current_user, user_login

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: CreateUser,
    db: Session = Depends(get_db),
) -> CreatedUserData:
    return await create_user(db=db, user_data=user_data)


@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
)
async def login(
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> AuthGrantedData:
    return await user_login(db=db, auth_data=auth_data)


@router.post(
    path="/me",
    status_code=status.HTTP_200_OK,
)
async def get_user_data(
    data: UserMeRequestData,
    db: Session = Depends(get_db),
):
    return await get_current_user(access_token=data.access_token, db=db)
