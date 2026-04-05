from typing import Protocol

from cleanstack.domain import SyncRepositoryProtocol

from app.domain.users.entities import User


class UserRepositoryProtocol(SyncRepositoryProtocol[User], Protocol):
    def get_by_provider_id(self, provider_id: str, /) -> User | None: ...
