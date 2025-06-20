import uuid
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
import typer
from bson import ObjectId
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient
from typer.testing import CliRunner

from app.api.app import create_app
from app.cli.app import create_cli_app
from app.core.config import DatabaseType, Settings
from app.core.context.sql import SqlContext
from app.domain.domain import Domain
from app.domain.entities import EntityId

pytest_plugins = [
    "tests.fixtures.database.sql",
    "tests.fixtures.database.mongo",
    "tests.fixtures.factories.fixtures",
]

project_dir = Path(__file__).parents[1]


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings_ = Settings(_env_file=project_dir / ".env.test")
    SqlContext.initialize(settings=settings_)
    return settings_


@pytest.fixture
def fake_entity_id(settings: Settings) -> EntityId:
    match settings.database_type:
        case DatabaseType.SQL:
            return str(uuid.uuid4())
        case DatabaseType.MONGO:
            return str(ObjectId())


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


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli_app(settings: Settings) -> typer.Typer:
    context = SqlContext()
    domain = Domain(context=context)
    return create_cli_app(domain=domain)
