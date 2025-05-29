from typing import TypeVar

from pymongo.collection import Collection

from app.domain.entities import DomainModel
from app.infrastructure.mongo.base import MongoDocument
from tests.fixtures.factories.base import BaseFactory

T = TypeVar("T", bound=DomainModel)


class MongoBaseFactory(BaseFactory[T, MongoDocument]):
    def __init__(self, collection: Collection[MongoDocument]):
        super().__init__()
        self.collection = collection

    def _insert(self, entities: list[T]) -> None:
        for entity in entities:
            db_entity = self._to_database_entity(entity)
            result = self.collection.insert_one(db_entity)
            entity.id = str(result.inserted_id)

    def _to_database_entity(self, entity: T, /) -> MongoDocument:
        return entity.model_dump(exclude={"id"})
