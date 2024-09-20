from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.core.database import get_db

router = APIRouter(tags=["Health Checks"])


@router.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
)
async def healthcheck(db: Session = Depends(get_db)) -> dict:
    try:
        await db.execute(text("SELECT 1"))
        return {"PostgreSQL": "healthy"}
    except OperationalError:
        return {"PostgreSQL": "unhealthy"}
