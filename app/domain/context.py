from typing import Protocol

from cleanstack.context import BaseContextProtocol

from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(BaseContextProtocol, Protocol):
    @property
    def cache_manager(self) -> CacheManagerProtocol: ...

    @property
    def dummy_repository(self) -> DummyRepositoryProtocol: ...

    @property
    def post_repository(self) -> PostRepositoryProtocol: ...

    @property
    def user_repository(self) -> UserRepositoryProtocol: ...

    @property
    def item_relational_repository(self) -> ItemRepositoryProtocol: ...

    @property
    def item_document_repository(self) -> ItemRepositoryProtocol: ...
