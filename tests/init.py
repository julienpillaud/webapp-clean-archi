from functools import lru_cache

from fastapi import FastAPI

from app.core.config import Settings
from app.core.context.context import Context
from app.domain.domain import Domain
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.infrastructure.cache_manager.inmemory_cache_manager import InMemoryCacheManager


class ContextTest(Context):
    @property
    def cache_manager(self) -> CacheManagerProtocol:
        return InMemoryCacheManager()


@lru_cache(maxsize=1)
def get_test_settings() -> Settings:
    return Settings(
        environment="test",
        jwt_secret="secret",
        jwt_audience="authenticated",
        postgres_user="user",
        postgres_password="password",
        postgres_host="localhost",
        postgres_db="database",
        redis_host="localhost",
    )


def get_test_domain(settings: Settings) -> Domain:
    context = ContextTest(settings=settings)
    return Domain(context=context)


def initialize_test_app(settings: Settings, app: FastAPI) -> None:
    domain = get_test_domain(settings=settings)
    app.state.domain = domain
