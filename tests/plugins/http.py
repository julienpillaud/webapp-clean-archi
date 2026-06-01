from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.app import create_fastapi_app
from app.api.security import encode_jwt
from app.core.config import Settings
from app.dependencies.fastapi.dependencies import get_context
from app.dependencies.settings import get_settings
from tests.context import get_context_override
from tests.plugins.factories import Factory
from tests.plugins.settings import get_settings_override


@pytest.fixture
def token(factory: Factory, settings: Settings) -> str:
    user = factory.users.create_one()
    return encode_jwt(
        sub=user.provider_id,
        email=user.email,
        settings=settings,
    )


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_context] = get_context_override
    return app


@pytest.fixture
def client(app: FastAPI, token: str) -> Iterator[TestClient]:
    with TestClient(app) as client:
        client.headers["Authorization"] = f"Bearer {token}"
        yield client
