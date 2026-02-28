from collections.abc import Iterator

import pytest
from cleanstack.infrastructure.mongodb.uow import MongoDBContext

from app.core.config import Settings


@pytest.fixture(scope="session")
def mongo_context_init(settings: Settings) -> MongoDBContext:
    return MongoDBContext.from_settings(
        host=settings.mongo_uri,
        database_name=settings.mongo_database,
    )


@pytest.fixture
def mongo_context(mongo_context_init: MongoDBContext) -> Iterator[MongoDBContext]:
    yield mongo_context_init

    database = mongo_context_init.database
    for collection in database.list_collection_names():
        database.drop_collection(collection)
