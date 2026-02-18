from functools import cached_property

from app.core.config import Settings
from app.core.logger import logger
from app.core.uow import UnitOfWork
from app.domain.context import ContextProtocol
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.cache_manager.redis_cache_manager import RedisCacheManager
from app.infrastructure.mongo.repositories.items import ItemMongoRepository
from app.infrastructure.sql.repositories.dummies import DummySQLRepository
from app.infrastructure.sql.repositories.items import ItemSQLRepository
from app.infrastructure.sql.repositories.posts import PostSQLRepository
from app.infrastructure.sql.repositories.users import UserSQLRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings, uow: UnitOfWork):
        logger.debug("Initializing context")
        self.settings = settings
        self.uow = uow

    @cached_property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(settings=self.settings)

    @cached_property
    def dummy_repository(self) -> DummyRepositoryProtocol:
        return DummySQLRepository(session=self.uow.sql.session)

    @cached_property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSQLRepository(session=self.uow.sql.session)

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(session=self.uow.sql.session)

    @cached_property
    def item_relational_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.uow.sql.session)

    @cached_property
    def item_document_repository(self) -> ItemRepositoryProtocol:
        return ItemMongoRepository(
            database=self.uow.mongo.database,
            session=self.uow.mongo.session,
        )
