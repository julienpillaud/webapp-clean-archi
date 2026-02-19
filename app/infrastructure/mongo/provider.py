from pymongo import MongoClient

from app.core.config import Settings
from app.infrastructure.mongo.base import MongoDocument
from app.infrastructure.mongo.logger import logger


class MongoProvider:
    _client: MongoClient[MongoDocument] | None = None

    @classmethod
    def init(cls, settings: Settings, /) -> None:
        if cls._client is None:
            logger.debug("Initializing MongoDB client")
            cls._client = MongoClient(
                settings.mongo_uri,
                uuidRepresentation="standard",
            )

    @classmethod
    def get_client(cls) -> MongoClient[MongoDocument]:
        if cls._client is None:
            raise RuntimeError("Not initialized.")
        return cls._client
