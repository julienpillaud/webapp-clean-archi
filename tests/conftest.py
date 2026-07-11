from functools import lru_cache

from pydantic import SecretStr

from app.core.config import Settings

pytest_plugins = [
    "tests.plugins.database",
    "tests.plugins.factories",
    "tests.plugins.http",
    "tests.plugins.repositories",
    "tests.plugins.settings",
]


@lru_cache
def get_settings_override() -> Settings:
    return Settings(
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="test",
    )
