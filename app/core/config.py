from typing import Any

from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
    )

    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str
    postgres_params: dict[str, Any] = {
        "pool_size": 20,
        "max_overflow": 50,
    }

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )
