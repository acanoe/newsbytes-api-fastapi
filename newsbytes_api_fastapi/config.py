import secrets
from typing import Any, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: list[AnyHttpUrl] = []

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "newsbytes"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_DSN: Optional[PostgresDsn] = None

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        """
        Assemble CORS_ORIGINS from comma-separated string or list of strings
        """

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DB_DSN", pre=True)
    def assemble_db_dsn(
        cls, v: Optional[str], values: dict[str, Any]
    ) -> Optional[PostgresDsn]:
        if isinstance(v, str):
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("DB_USER"),
                password=values.get("DB_PASSWORD"),
                host=values.get("DB_HOST"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME')}",
            )
        return v


settings = Settings()
