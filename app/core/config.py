from enum import StrEnum
from typing import Self, assert_never

from pydantic import PostgresDsn, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseType(StrEnum):
    SQL = "sql"
    MONGO = "mongo"


required_fields = {
    DatabaseType.SQL: [
        "postgres_user",
        "postgres_password",
        "postgres_host",
        "postgres_db",
    ],
    DatabaseType.MONGO: [
        "mongo_user",
        "mongo_password",
        "mongo_host",
        "mongo_database",
    ],
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    project_name: str = "webapp-clean-archi"
    api_version: str = "0.0.1"
    environment: str
    database_type: DatabaseType = DatabaseType.SQL

    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: str
    logfire_token: str = ""

    postgres_user: str = ""
    postgres_password: str = ""
    postgres_host: str = ""
    postgres_port: int = 5432
    postgres_db: str = ""

    mongo_user: str = ""
    mongo_password: str = ""
    mongo_host: str = ""
    mongo_port: int = 27017
    mongo_database: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_uri(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def mongo_uri(self) -> str:
        if self.mongo_host == "localhost":
            return (
                f"mongodb://{self.mongo_user}:{self.mongo_password}"
                f"@{self.mongo_host}:{self.mongo_port}"
            )
        else:
            return (
                f"mongodb+srv://{self.mongo_user}:{self.mongo_password}"
                f"@{self.mongo_host}/?retryWrites=true&w=majority"
            )

    @model_validator(mode="after")
    def validate_required_fields(self) -> Self:
        match self.database_type:
            case DatabaseType.SQL:
                required = required_fields[DatabaseType.SQL]
            case DatabaseType.MONGO:
                required = required_fields[DatabaseType.MONGO]
            case _:
                assert_never(DatabaseType)

        if [field for field in required if not getattr(self, field)]:
            raise ValueError("Missing required fields")

        return self
