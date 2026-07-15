from functools import cached_property

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.domain.synchronous import TransactionProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.items import ItemSQLRepository
from app.infrastructure.sql.posts import PostSQLRepository
from app.infrastructure.sql.resource import SQLTransaction
from app.infrastructure.sql.users import UserSQLRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings, transaction: SQLTransaction) -> None:
        self.settings = settings
        self.transaction = transaction

    @property
    def session(self) -> Session:
        if self.transaction.session is None:
            raise RuntimeError()
        return self.transaction.session

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

    def __call__(self, transaction: TransactionProtocol) -> Context:
        if not isinstance(transaction, SQLTransaction):
            raise RuntimeError()

        return Context(settings=self._settings, transaction=transaction)
