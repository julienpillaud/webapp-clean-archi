from pydantic import AmqpDsn, PostgresDsn, RedisDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
    )

    project_name: str = "webapp-clean-archi"
    api_version: str = "0.0.1"
    environment: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_audience: str

    logfire_token: str = ""

    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str

    mongo_host: str
    mongo_port: int = 27017
    mongo_rs_name: str = "rs0"
    mongo_database: str

    redis_host: str
    redis_port: int = 6379
    redis_db: str = "0"

    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_host: str
    rabbitmq_port: int = 5672
    rabbitmq_vhost: str = "/"

    @computed_field  # type: ignore
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

    @computed_field  # type: ignore
    @property
    def mongo_uri(self) -> str:
        return (
            f"mongodb://"
            f"{self.mongo_host}:{self.mongo_port}/"
            f"?replicaSet={self.mongo_rs_name}"
        )

    @computed_field  # type: ignore
    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            path=self.redis_db,
        )

    @computed_field  # type: ignore
    @property
    def rabbitmq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.rabbitmq_user,
            password=self.rabbitmq_password,
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            path=self.rabbitmq_vhost,
        )
