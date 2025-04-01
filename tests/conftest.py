import pathlib
from collections.abc import Iterator

import pytest
from starlette.testclient import TestClient

from app.api.dependencies import get_settings
from app.core.app import app
from app.core.config import Settings

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    project_path = pathlib.Path(__file__).parent.parent
    env_file = project_path / "tests/.env.test"
    return Settings(_env_file=env_file)  # type: ignore


@pytest.fixture(scope="session")
def client(settings: Settings) -> Iterator[TestClient]:
    def get_settings_override() -> Settings:
        return settings

    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app)
    app.dependency_overrides.clear()
