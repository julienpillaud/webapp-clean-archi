from functools import lru_cache

import pytest
from pydantic import SecretStr

from app.core.config import Settings


@lru_cache
def get_settings_override() -> Settings:
    return Settings(
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="test",
    )


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()
