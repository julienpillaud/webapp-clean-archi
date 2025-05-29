from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from pymongo.synchronous.database import Database

from app.core.config import Settings
from app.infrastructure.mongo.base import MongoDocument


@pytest.fixture
def mongo_db(settings: Settings) -> Iterator[Database[MongoDocument]]:
    client: MongoClient[MongoDocument] = MongoClient(settings.mongo_uri)
    database: Database[MongoDocument] = client[settings.mongo_database]

    yield database

    for collection in database.list_collection_names():
        database[collection].delete_many({})
    client.close()
