import logging
import uuid
from collections.abc import AsyncIterator, Iterator
from functools import lru_cache
from pathlib import Path

import pytest
import typer
from bson import ObjectId
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from typer.testing import CliRunner

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.cli.app import create_cli_app
from app.core.config import DatabaseType, Settings
from app.core.context.sql import SqlContext
from app.core.security import create_access_token
from app.domain.domain import Domain
from app.domain.entities import EntityId
from tests.fixtures.factories.users.base import UserBaseFactory

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database.sql",
    "tests.fixtures.database.mongo",
    "tests.fixtures.factories.fixtures",
]

project_dir = Path(__file__).parents[1]


@lru_cache(maxsize=1)
def get_test_settings() -> Settings:
    return Settings(_env_file=project_dir / ".env.test")


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings_ = get_test_settings()
    logger.info(f"Loading settings for {settings_.environment} environment")
    SqlContext.initialize(settings=settings_)
    return settings_


@pytest.fixture
def fake_entity_id(settings: Settings) -> EntityId:
    match settings.database_type:
        case DatabaseType.SQL:
            return str(uuid.uuid4())
        case DatabaseType.MONGO:
            return str(ObjectId())


@pytest.fixture
def client(user_factory: UserBaseFactory, settings: Settings) -> Iterator[TestClient]:
    user = user_factory.create_one()
    token_data = create_access_token(settings=settings, subject=user.id)

    app = create_app(settings=settings)
    app.dependency_overrides[get_settings] = get_test_settings

    client = TestClient(app)
    client.headers["Authorization"] = f"Bearer {token_data.access_token}"
    yield client


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
