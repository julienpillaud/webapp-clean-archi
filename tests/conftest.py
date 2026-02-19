import json
import logging
import logging.config
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path

import pytest
import typer
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr
from typer.testing import CliRunner

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.api.security import encode_jwt
from app.cli.app import create_cli_app
from app.core.config import Settings
from tests.factories.users import UserSQLFactory

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]


@lru_cache(maxsize=1)
def get_test_settings() -> Settings:
    return Settings(
        environment="test",
        jwt_secret="secret",
        jwt_audience="authenticated",
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="test",
        redis_host="localhost",
        mongo_host="localhost",
        mongo_database="test",
    )


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_test_settings()


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
    app = create_app(settings=settings)
    app.dependency_overrides[get_settings] = get_test_settings
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
