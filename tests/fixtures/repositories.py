import pytest
from pymongo.database import Database

from app.infrastructure.mongo.base import MongoDocument
from app.infrastructure.mongo.generics import GenericEntityMongoRepository


@pytest.fixture
def generic_entity_mongo_repository(
    mongo_db: Database[MongoDocument],
) -> GenericEntityMongoRepository:
    return GenericEntityMongoRepository(database=mongo_db)
