from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
    db: Session = Depends(get_db),
) -> UserMeData:
    return await get_current_user(db=db, access_token=data.access_token)
