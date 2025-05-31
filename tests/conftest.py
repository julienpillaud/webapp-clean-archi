from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from app.api.app import create_app
from app.core.config import Settings
from app.core.context.utils import initialize_context

pytest_plugins = [
    "tests.fixtures.database.sql",
    "tests.fixtures.database.mongo",
    "tests.fixtures.repositories",
    "tests.fixtures.factories.fixtures",
]

project_dir = Path(__file__).parents[1]


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings_ = Settings(_env_file=project_dir / ".env.test")
    initialize_context(settings=settings_)
    return settings_


@pytest.fixture(scope="session")
def client(settings: Settings) -> Iterator[TestClient]:
    app = create_app(settings=settings)
    yield TestClient(app)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client_async(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings=settings)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
