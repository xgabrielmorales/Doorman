from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.apps.healthcheck.schemas import HealthCheckData
from src.core.database import get_db

router = APIRouter(tags=["Health Check"])


@router.get(
    path="/healthcheck",
    status_code=status.HTTP_200_OK,
)
async def healthcheck(db: Session = Depends(get_db)) -> HealthCheckData:
    try:
        await db.execute(text("SELECT 1"))
        response = HealthCheckData(PostgreSQL="healthy")
    except OperationalError:
        response = HealthCheckData(PostgreSQL="unhealthy")

    return response
