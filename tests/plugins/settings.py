import pytest
from pydantic import SecretStr

from app.core.config import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="test",
    )
