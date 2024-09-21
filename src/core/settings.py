from typing import Optional, Union

from pydantic import ValidationInfo, field_validator
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY: str = "3RWM3zT68QEaOacQiYmSVzNyOHnJMpqVQi8mS2zN"

    POSTGRES_HOST: str = "postgres-db"
    POSTGRES_DB: str = "example-db-db"
    POSTGRES_USER: str = "example-user-db"
    POSTGRES_PASSWORD: str = "example-password-db"
    POSTGRES_URL: Union[PostgresDsn, str, None] = None

    @field_validator("POSTGRES_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        url = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.data["POSTGRES_HOST"],
            password=values.data["POSTGRES_PASSWORD"],
            username=values.data["POSTGRES_USER"],
            path=values.data["POSTGRES_DB"],
        )

        return str(url)


settings = Settings()
