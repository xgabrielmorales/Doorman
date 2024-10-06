from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.users.schemas import (
    CreatedUserData,
    CreateUserData,
    UserMeData,
)
from src.apps.users.services import create_user, get_current_user
from src.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


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
    path="/me",
    status_code=status.HTTP_200_OK,
)
async def get_user_data(
    current_user: Annotated[UserMeData, Depends(get_current_user)],
) -> UserMeData:
    return current_user
