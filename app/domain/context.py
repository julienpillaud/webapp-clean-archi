from typing import Protocol

from app.domain.items.repository import ItemRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def post_repository(self) -> PostRepositoryProtocol: ...

    @property
    def user_repository(self) -> UserRepositoryProtocol: ...

    @property
    def item_repository(self) -> ItemRepositoryProtocol: ...
