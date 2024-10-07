from fastapi import FastAPI

from src.apps.healthcheck.routers import router as healthcheck_router
from src.apps.user.routers import router as user_router

app = FastAPI(title="Persona Keeper", version="0.1.0")
app.include_router(healthcheck_router)
app.include_router(user_router)
