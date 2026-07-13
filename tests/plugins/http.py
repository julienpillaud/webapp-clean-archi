from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.app import create_fastapi_app
from app.api.dependencies import get_settings
from app.core.config import Settings
from app.infrastructure.sql.utils import SQLResource
from tests.conftest import get_settings_override


@pytest.fixture
def app(settings: Settings, db_resource: SQLResource) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = get_settings_override
    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client
