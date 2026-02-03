from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def cache_manager(self) -> CacheManagerProtocol: ...

    @property
    def dummy_repository(self) -> DummyRepositoryProtocol: ...

    @property
    def post_repository(self) -> PostRepositoryProtocol: ...

    @property
    def user_repository(self) -> UserRepositoryProtocol: ...
