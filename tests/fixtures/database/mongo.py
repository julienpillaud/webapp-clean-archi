from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from pymongo.synchronous.database import Database

from app.core.config import Settings
from app.infrastructure.mongo.base import MongoDocument


@pytest.fixture
def mongo_db(settings: Settings) -> Iterator[Database[MongoDocument]]:
    client: MongoClient[MongoDocument] = MongoClient(
        settings.mongo_uri, uuidRepresentation="standard"
    )
    database: Database[MongoDocument] = client[settings.mongo_database]

    yield database

    for collection in database.list_collection_names():
        database[collection].delete_many({})
    client.close()


@pytest.fixture
def mongo_text_indexes(mongo_db: Database[MongoDocument]) -> None:
    mongo_db["posts"].create_index([("title", "text"), ("content", "text")])
