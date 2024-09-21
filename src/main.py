from fastapi import FastAPI

from src.apps.authentication.routers import router as authentication_router
from src.apps.healthcheck.routers import router as healthcheck_router
from src.apps.users.routers import router as users_router

app = FastAPI(title="My APP", version="0.1.0")

app.include_router(healthcheck_router)
app.include_router(authentication_router)
app.include_router(users_router)
