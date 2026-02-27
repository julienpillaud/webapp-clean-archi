from collections.abc import Iterator

import pytest

from app.core.config import Settings
from app.infrastructure.mongo.uow import MongoContext


@pytest.fixture(scope="session")
def mongo_context_init(settings: Settings) -> MongoContext:
    return MongoContext.from_settings(
        uri=settings.mongo_uri,
        database_name=settings.mongo_database,
    )


@pytest.fixture
def mongo_context(mongo_context_init: MongoContext) -> Iterator[MongoContext]:
    yield mongo_context_init

    database = mongo_context_init.database
    for collection in database.list_collection_names():
        database.drop_collection(collection)
