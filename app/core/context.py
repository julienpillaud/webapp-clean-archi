from functools import cached_property

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.domain.synchronous import ResourceProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.items import ItemSQLRepository
from app.infrastructure.sql.posts import PostSQLRepository
from app.infrastructure.sql.resource import SQLResource
from app.infrastructure.sql.users import UserSQLRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings, resource: SQLResource) -> None:
        self.settings = settings
        self.resource = resource

    @property
    def session(self) -> Session:
        if self.resource.session is None:
            raise RuntimeError()
        return self.resource.session

    @cached_property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSQLRepository(session=self.session)

    @cached_property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSQLRepository(session=self.session)

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.session)


class ContextProvider:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def __call__(self, resource: ResourceProtocol) -> Context:
        if not isinstance(resource, SQLResource):
            raise RuntimeError()

        return Context(settings=self._settings, resource=resource)
