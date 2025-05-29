from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.core.config import Settings
from app.core.context.sql import Context

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]

project_dir = Path(__file__).parents[1]


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings_ = Settings(_env_file=project_dir / ".env.test")
    Context.initialize(settings=settings_)
    return settings_


@pytest.fixture(scope="session")
def client(settings: Settings) -> Iterator[TestClient]:
    def get_settings_override() -> Settings:
        return settings

    app = create_app(settings=settings)

    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client_async(settings: Settings) -> AsyncIterator[AsyncClient]:
    def get_settings_override() -> Settings:
        return settings

    app = create_app(settings=settings)

    app.dependency_overrides[get_settings] = get_settings_override

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()
