from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.apps.authentication.routers import router as authentication_router
from src.apps.authentication.services.jwt_exceptions import AuthJwtException
from src.apps.healthcheck.routers import router as healthcheck_router
from src.apps.users.routers import router as users_router

app = FastAPI(title="My APP", version="0.1.0")


@app.exception_handler(AuthJwtException)
def authjwt_exception_handler(request: Request, exc: AuthJwtException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(healthcheck_router)
app.include_router(authentication_router)
app.include_router(users_router)
