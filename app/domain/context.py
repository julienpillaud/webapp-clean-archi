from typing import Protocol

from app.domain.post.repository import PostRepositoryProtocol
from app.domain.user.repository import UserRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def post_repository(self) -> PostRepositoryProtocol: ...
    @property
    def user_repository(self) -> UserRepositoryProtocol: ...
