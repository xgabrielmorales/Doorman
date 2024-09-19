from src.routers.auth import router as auth_router
from src.routers.healthcheck import router as healthcheck_router

__all__ = (
    "auth_router",
    "healthcheck_router",
)
