from pymongo.client_session import ClientSession

from app.core.config import Settings
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
from app.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from app.infrastructure.sql.repositories.dummies import DummySQLRepository
from app.infrastructure.sql.repositories.items import ItemSQLRepository
from app.infrastructure.sql.repositories.posts import PostSQLRepository
from app.infrastructure.sql.repositories.users import UserSQLRepository
from app.infrastructure.sql.uow import SQLUnitOfWork


class Context(ContextProtocol):
    def __init__(
        self,
        settings: Settings,
        sql_uow: SQLUnitOfWork,
        mongo_context: MongoContext,
        mongo_uow: MongoUnitOfWork | None = None,
    ):
        self.settings = settings
        self.sql_uow = sql_uow
        self.mongo_context = mongo_context
        self.mongo_uow = mongo_uow

    @property
    def _mongo_session(self) -> ClientSession | None:
        return self.mongo_uow.session if self.mongo_uow else None

    @property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(settings=self.settings)

    @property
    def event_publisher(self) -> EventPublisherProtocol:
        return FastStreamEventPublisher(settings=self.settings)

    @property
    def dummy_repository(self) -> DummyRepositoryProtocol:
        return DummySQLRepository(session=self.sql_uow.session)

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSQLRepository(session=self.sql_uow.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(session=self.sql_uow.session)

    @property
    def item_relational_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.sql_uow.session)

    @property
    def item_document_repository(self) -> ItemRepositoryProtocol:
        return ItemMongoRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )
