from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.apps.users.schemas import UserMeData
from src.apps.users.services import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    path="/me",
    status_code=status.HTTP_200_OK,
)
async def get_user_data(
    current_user: Annotated[UserMeData, Depends(get_current_user)],
) -> UserMeData:
    return current_user
