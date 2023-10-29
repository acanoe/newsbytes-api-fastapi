import secrets
from typing import Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
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
    DB_PASS: str = "postgres"

    @field_validator("CORS_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        """
        Assemble CORS_ORIGINS from comma-separated string or list of strings
        """

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @property
    def DB_DSN(self) -> Optional[PostgresDsn]:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
