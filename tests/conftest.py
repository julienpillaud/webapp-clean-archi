from collections.abc import Iterator
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.core.config import Settings

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]

project_dir = Path(__file__).parents[1]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(_env_file=project_dir / ".env.test")


@pytest.fixture(scope="session")
def client(settings: Settings) -> Iterator[TestClient]:
    def get_settings_override() -> Settings:
        return settings

    app = create_app(settings=settings)

    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app)
    app.dependency_overrides.clear()
