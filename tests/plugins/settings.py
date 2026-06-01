import secrets
from functools import lru_cache

import pytest
from pydantic import SecretStr

from app.core.config import Settings


@lru_cache
def get_settings_override() -> Settings:
    return Settings(
        environment="test",
        jwt_secret=secrets.token_hex(32),
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


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()
