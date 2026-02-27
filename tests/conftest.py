import json
import logging
import logging.config
from collections.abc import Iterator
from pathlib import Path

import pytest
import typer
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from app.api.app import create_fastapi_app
from app.api.security import encode_jwt
from app.cli.app import create_cli_app
from app.core.config import Settings
from tests.dependencies.dependencies import get_settings_override
from tests.dependencies.fastapi import apply_fastapi_overrides
from tests.dependencies.faststream import apply_faststream_overrides
from tests.factories.users import UserSQLFactory

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.sql",
    "tests.fixtures.mongo",
    "tests.fixtures.factories",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()


@pytest.fixture
def token(user_factory: UserSQLFactory, settings: Settings) -> str:
    user = user_factory.create_one()
    return encode_jwt(
        sub=user.provider_id,
        email=user.email,
        settings=settings,
    )


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    apply_fastapi_overrides(app=app)
    apply_faststream_overrides()
    return app


@pytest.fixture
def client(app: FastAPI, token: str) -> Iterator[TestClient]:
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
    return create_cli_app(settings=settings)
