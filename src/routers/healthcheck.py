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
async def healthcheck(postgres_db: Session = Depends(get_db)) -> dict:
    try:
        await postgres_db.execute(text("SELECT 1"))
        postgres_status = "ok"
    except OperationalError:
        postgres_status = "error"

    return {
        "PostgreSQL": postgres_status,
    }
