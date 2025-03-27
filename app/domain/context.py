from typing import Protocol

from app.domain.user.repository import UserRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def user_repository(self) -> UserRepositoryProtocol: ...
