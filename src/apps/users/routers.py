from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.users.schemas import UserMeData, UserMeRequestData
from src.apps.users.services import get_current_user
from src.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    path="/me",
    status_code=status.HTTP_200_OK,
)
async def get_user_data(
    data: UserMeRequestData,
    db: AsyncSession = Depends(get_db),
) -> UserMeData:
    user = await get_current_user(db=db, access_token=data.access_token)
    return UserMeData.model_validate(user)
