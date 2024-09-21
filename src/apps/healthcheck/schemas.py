from typing import Literal

from pydantic import BaseModel


class HealthCheckData(BaseModel):
    PostgreSQL: Literal["healthy", "unhealthy"]
