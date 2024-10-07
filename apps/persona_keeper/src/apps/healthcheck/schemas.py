from typing import Literal

from pydantic import BaseModel


class HealthCheckData(BaseModel):
    app: Literal["healthy", "unhealthy"]
    postgresql: Literal["healthy", "unhealthy"]
