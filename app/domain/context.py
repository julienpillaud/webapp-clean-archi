from typing import Protocol

from app.core.config import Settings
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(Protocol):
    @classmethod
    def initialize(cls, settings: Settings) -> None: ...
    @property
    def post_repository(self) -> PostRepositoryProtocol: ...
    @property
    def user_repository(self) -> UserRepositoryProtocol: ...
