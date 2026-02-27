from functools import cached_property

from app.core.config import Settings
from app.core.logger import logger
from app.core.uow import UnitOfWork
from app.domain.context import ContextProtocol
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.domain.interfaces.event_publisher import EventPublisherProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.cache_manager.redis_cache_manager import RedisCacheManager
from app.infrastructure.event_publisher.faststream_event_publisher import (
    FastStreamEventPublisher,
)
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
    def event_publisher(self) -> EventPublisherProtocol:
        return FastStreamEventPublisher(settings=self.settings)

    @cached_property
    def dummy_repository(self) -> DummyRepositoryProtocol:
        return DummySQLRepository(uow=self.uow.sql)

    @cached_property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSQLRepository(uow=self.uow.sql)

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(uow=self.uow.sql)

    @cached_property
    def item_relational_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(uow=self.uow.sql)

    @cached_property
    def item_document_repository(self) -> ItemRepositoryProtocol:
        return ItemMongoRepository(uow=self.uow.mongo)
