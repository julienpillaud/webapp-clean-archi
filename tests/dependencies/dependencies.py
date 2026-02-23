from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import SecretStr

from app.api.dependencies import get_uow
from app.core.config import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from tests.context import ContextTest


@lru_cache(maxsize=1)
def get_settings_override() -> Settings:
    return Settings(
        environment="test",
        jwt_secret="secret",
        jwt_audience="authenticated",
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="test",
        mongo_host="localhost",
        mongo_database="test",
        redis_host="localhost",
        rabbitmq_user="user",
        rabbitmq_password="password",
        rabbitmq_host="localhost",
    )


def get_context_override(
    settings: Annotated[Settings, Depends(get_settings_override)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> Context:
    return ContextTest(settings=settings, uow=uow)
