import logging
from functools import cached_property

from cleanstack.uow import CompositeUniOfWork
from redis import Redis

from app.core.config import Settings
from app.core.uows import SQLUnitOfWork
from app.domain.context import ContextProtocol
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.cache_manager.redis_cache_manager import RedisCacheManager
from app.infrastructure.sql.dummies import DummySqlRepository
from app.infrastructure.sql.posts import PostSqlRepository
from app.infrastructure.sql.users import UserSqlRepository

logger = logging.getLogger(__name__)


class Context(CompositeUniOfWork, ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        logger.debug("Initializing context...")
        self.sql_uow = SQLUnitOfWork(settings=settings)
        self.members = [self.sql_uow]

        self.redis_client = Redis.from_url(
            str(settings.redis_dsn),
            decode_responses=True,
        )

    @property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(client=self.redis_client)

    @property
    def dummy_repository(self) -> DummyRepositoryProtocol:
        return DummySqlRepository(session=self.sql_uow.session)

    @cached_property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSqlRepository(session=self.sql_uow.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSqlRepository(session=self.sql_uow.session)
