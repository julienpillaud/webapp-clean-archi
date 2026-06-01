from functools import cached_property

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.domain.context import ContextProtocol
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.domain.interfaces.event_publisher import EventPublisherProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.cache_manager.redis_cache_manager import RedisCacheManager
from app.infrastructure.event_publisher.faststream_event_publisher import (
    FastStreamEventPublisher,
)
from app.infrastructure.sql.posts import PostSQLRepository
from app.infrastructure.sql.users import UserSQLRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings, session: Session) -> None:
        self.settings = settings
        self.session = session

    @cached_property
    def cache_manager(self) -> CacheManagerProtocol:
        return RedisCacheManager(settings=self.settings)

    @cached_property
    def event_publisher(self) -> EventPublisherProtocol:
        return FastStreamEventPublisher(settings=self.settings)

    @cached_property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSQLRepository(session=self.session)

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(session=self.session)
