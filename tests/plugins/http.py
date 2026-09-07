from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.app import create_fastapi_app
from app.api.dependencies import get_settings
from app.core.config import Settings
from app.infrastructure.sql.resource import SQLTransaction


class SettingsOverride:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def __call__(self) -> Settings:
        return self.settings


@pytest.fixture
def app(settings: Settings, db_resource: SQLTransaction) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = SettingsOverride(settings=settings)
    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client
