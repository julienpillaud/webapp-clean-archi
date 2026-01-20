import json
import logging
import logging.config
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path

import pytest
import typer
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.cli.app import create_cli_app
from app.core.config import Settings
from app.core.context.context import Context
from app.core.core import initialize_app
from app.core.security import create_access_token
from app.domain.domain import Domain
from tests.factories.users import UserFactory

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]

project_dir = Path(__file__).parents[1]


@lru_cache(maxsize=1)
def get_test_settings() -> Settings:
    settings_ = Settings(_env_file=project_dir / ".env.test")  # ty:ignore[unknown-argument,missing-argument]
    logger.info(f"Loading settings for ENV {settings_.environment}")
    return settings_


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_test_settings()


@pytest.fixture
def client(user_factory: UserFactory, settings: Settings) -> Iterator[TestClient]:
    user = user_factory.create_one()
    token_data = create_access_token(settings=settings, subject=user.id)

    app = create_app(settings=settings)
    initialize_app(settings=settings, app=app)
    app.dependency_overrides[get_settings] = get_test_settings

    client = TestClient(app)
    client.headers["Authorization"] = f"Bearer {token_data.access_token}"
    yield client


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli_app(settings: Settings) -> typer.Typer:
    config = json.loads(Path("app/core/logging/config.json").read_text())
    logging.config.dictConfig(config)
    context = Context(settings=settings)
    domain = Domain(context=context)
    return create_cli_app(domain=domain)
