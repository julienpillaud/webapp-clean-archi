from collections.abc import Iterator
from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.mongo.base import MongoDocument
from app.infrastructure.mongo.posts import PostMongoRepository
from app.infrastructure.mongo.users import UserMongoRepository


class MongoContext(TransactionalContextProtocol):
    client: MongoClient[MongoDocument] | None = None
    _database: Database[MongoDocument] | None = None

    @classmethod
    def initialize(cls, settings: Settings) -> None:
        cls.client = MongoClient(settings.mongo_uri)
        cls._database = cls.client[settings.mongo_database]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    @property
    def database(self) -> Database[MongoDocument]:
        if self._database is None:
            raise RuntimeError("Database not initialized.")
        return self._database

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostMongoRepository(database=self.database)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserMongoRepository(database=self.database)
