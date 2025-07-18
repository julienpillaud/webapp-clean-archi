from enum import StrEnum
from typing import Self

from pydantic import AmqpDsn, PostgresDsn, SecretStr, computed_field, model_validator
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
    model_config = SettingsConfigDict(extra="ignore", frozen=True, env_file=".env")

    project_name: str = "webapp-clean-archi"
    api_version: str = "0.0.1"
    environment: str
    database_type: DatabaseType = DatabaseType.SQL

    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: str
    logfire_token: str = ""

    rabbitmq_default_user: str
    rabbitmq_default_pass: SecretStr
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_vhost: str = "/"

    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int
    postgres_db: str

    mongo_user: str
    mongo_password: SecretStr
    mongo_host: str
    mongo_port: int
    mongo_database: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def broker_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.rabbitmq_default_user,
            password=self.rabbitmq_default_pass.get_secret_value(),
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            path=self.rabbitmq_vhost,
        )

    @computed_field  # type: ignore[prop-decorator]
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

    @computed_field  # type: ignore[prop-decorator]
    @property
    def mongo_uri(self) -> str:
        if self.mongo_host == "localhost":
            return (
                f"mongodb://"
                f"{self.mongo_user}:{self.mongo_password.get_secret_value()}"
                f"@{self.mongo_host}:{self.mongo_port}"
            )
        else:
            return (
                f"mongodb+srv://"
                f"{self.mongo_user}:{self.mongo_password.get_secret_value()}"
                f"@{self.mongo_host}/?retryWrites=true&w=majority"
            )

    @model_validator(mode="after")
    def validate_required_fields(self) -> Self:
        match self.database_type:
            case DatabaseType.SQL:
                required = required_fields[DatabaseType.SQL]
            case DatabaseType.MONGO:
                required = required_fields[DatabaseType.MONGO]

        if [field for field in required if not getattr(self, field)]:
            raise ValueError("Missing required fields")

        return self
