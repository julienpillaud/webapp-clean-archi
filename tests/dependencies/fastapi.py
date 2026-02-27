from typing import Annotated

from fastapi import Depends, FastAPI

from app.core.config import Settings
from app.core.uow import UnitOfWork
from app.dependencies.fastapi.dependencies import get_context, get_uow
from app.dependencies.settings import get_settings
from tests.context import ContextTest
from tests.dependencies.dependencies import get_settings_override


def get_context_override(
    settings: Annotated[Settings, Depends(get_settings_override)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> ContextTest:
    return ContextTest(settings=settings, uow=uow)


def apply_fastapi_overrides(app: FastAPI) -> None:
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_context] = get_context_override
