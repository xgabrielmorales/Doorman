from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.healthcheck.schemas import HealthCheckData
from src.core.database import get_db

router = APIRouter(tags=["Health Check"])


@router.get(
    path="/healthcheck",
    status_code=status.HTTP_200_OK,
)
async def healthcheck(db: AsyncSession = Depends(get_db)) -> HealthCheckData:
    try:
        (await db.exec(text("SELECT 1"))).first()
        postgres_status = "healthy"
    except OperationalError:
        postgres_status = "unhealthy"

    return HealthCheckData(
        app="healthy",
        postgresql=postgres_status,
    )
