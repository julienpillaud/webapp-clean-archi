import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv
from starlette.testclient import TestClient

from app.api.dependencies import get_settings
from app.core.app import app
from app.core.config import Settings

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]

load_dotenv()


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        POSTGRES_USER=os.getenv("POSTGRES_USER", "user"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "password"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost"),
        POSTGRES_PORT=int(os.getenv("POSTGRES_PORT_TEST", "5432")),
        POSTGRES_DB=os.getenv("POSTGRES_DB_TEST", "database"),
    )


@pytest.fixture(scope="session")
def client(settings: Settings) -> Iterator[TestClient]:
    def get_settings_override() -> Settings:
        return settings

    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app)
    app.dependency_overrides.clear()
