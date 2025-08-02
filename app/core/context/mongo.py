import logging
from collections.abc import Iterator
from contextlib import contextmanager

from pymongo import MongoClient

from app.core.config import Settings
from app.domain.context import ContextProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.mongo.base import MongoDocument
from app.infrastructure.mongo.posts import PostMongoRepository
from app.infrastructure.mongo.users import UserMongoRepository

logger = logging.getLogger(__name__)


class MongoContext(ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        logger.info("Creating Mongo context")
        self.client: MongoClient[MongoDocument] = MongoClient(
            settings.mongo_uri,
            uuidRepresentation="standard",
        )
        self.database = self.client[settings.mongo_database]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostMongoRepository(database=self.database)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserMongoRepository(database=self.database)
