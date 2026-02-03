import json
import logging
import logging.config
from collections.abc import Iterator
from pathlib import Path

import pytest
import typer
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.api.security import encode_jwt
from app.cli.app import create_cli_app
from app.core.config import Settings
from tests.factories.users import UserFactory
from tests.init import (
    get_test_domain,
    get_test_settings,
    initialize_test_app,
)

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_test_settings()


@pytest.fixture
def client(user_factory: UserFactory, settings: Settings) -> Iterator[TestClient]:
    user = user_factory.create_one()
    token = encode_jwt(
        sub=user.provider_id,
        email=user.email,
        settings=settings,
    )

    app = create_app(settings=settings)
    initialize_test_app(settings=settings, app=app)
    app.dependency_overrides[get_settings] = get_test_settings

    client = TestClient(app)
    client.headers["Authorization"] = f"Bearer {token}"
    yield client


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli_app(settings: Settings) -> typer.Typer:
    config = json.loads(Path("app/core/logging/config.json").read_text())
    logging.config.dictConfig(config)
    domain = get_test_domain(settings=settings)
    return create_cli_app(domain=domain)
