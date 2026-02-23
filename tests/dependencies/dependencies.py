from functools import lru_cache

from pydantic import SecretStr

from app.core.config import Settings


@lru_cache(maxsize=1)
def get_settings_override() -> Settings:
    return Settings(
        environment="test",
        jwt_secret="secret",
        jwt_audience="authenticated",
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="test",
        mongo_host="localhost",
        mongo_database="test",
        redis_host="localhost",
        rabbitmq_user="user",
        rabbitmq_password="password",
        rabbitmq_host="localhost",
    )
