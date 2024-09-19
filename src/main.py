from fastapi import FastAPI

from src.routers import auth_router, healthcheck_router

app = FastAPI(
    title="My APP",
    version="0.1.0",
)
app.include_router(healthcheck_router)
app.include_router(auth_router)
