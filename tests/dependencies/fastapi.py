from fastapi import FastAPI

from app.api.dependencies import get_context, get_settings
from tests.dependencies.dependencies import get_context_override, get_settings_override


def apply_fastapi_overrides(app: FastAPI) -> None:
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_context] = get_context_override
