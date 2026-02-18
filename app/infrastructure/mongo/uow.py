from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.uow import UnitOfWorkProtocol
from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.core.config import Settings
from app.infrastructure.mongo.base import MongoDocument
from app.infrastructure.mongo.provider import MongoProvider


class MongoUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings) -> None:
        MongoProvider.init(settings)
        self.client: MongoClient[MongoDocument] = MongoProvider.get_client()
        self.database = self.client[settings.mongo_database]
        self._session: ClientSession | None = None

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError("No active session.")
        return self._session

    @contextmanager
    def transaction(self) -> Iterator[None]:
        self._session = self.client.start_session()
        self._session.start_transaction()
        try:
            yield
        finally:
            self._session.end_session()
            self._session = None

    def commit(self) -> None:
        self.session.commit_transaction()

    def rollback(self) -> None:
        self.session.abort_transaction()
