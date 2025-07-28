from typing import Generic, TypeVar

from cleanstack.entities import DomainModel
from pymongo.collection import Collection

from app.infrastructure.mongo.base import MongoDocument
from factories.base import BaseFactory

T = TypeVar("T", bound=DomainModel)


class MongoBaseFactory(BaseFactory[T], Generic[T]):
    def __init__(self, collection: Collection[MongoDocument]):
        self.collection = collection

    def _insert_one(self, entity: T) -> None:
        db_entity = self._to_database_entity(entity)
        self.collection.insert_one(db_entity)

    def _to_database_entity(self, entity: T, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document
