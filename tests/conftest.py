import pathlib

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.api.app import app_factory
from app.core.config import Settings
from app.core.context import Context
from app.domain.domain import Domain, TransactionalContextProtocol

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
]


@pytest.fixture(scope="session")
def settings():
    project_path = pathlib.Path(__file__).parent.parent
    env_file = project_path / "tests/.env.test"
    return Settings(_env_file=env_file)  # type: ignore


@pytest.fixture(scope="session")
def context(settings: Settings):
    return Context(settings=settings)


@pytest.fixture(scope="session")
def domain(context: TransactionalContextProtocol):
    return Domain(context=context)


@pytest.fixture(scope="session")
def app(domain: Domain):
    return app_factory(domain=domain)


@pytest.fixture(scope="session")
def client(app: FastAPI):
    with TestClient(app) as client_:
        yield client_
