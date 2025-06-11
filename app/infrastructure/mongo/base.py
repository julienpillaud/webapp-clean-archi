from typing import Any, Generic, TypeVar

from bson import ObjectId
from pymongo.database import Database

from app.domain.entities import DomainModel, EntityId, PaginatedResponse, Pagination
from app.domain.interfaces.repository import BaseRepositoryProtocol

Domain_T = TypeVar("Domain_T", bound=DomainModel)


type MongoDocument = dict[str, Any]


class BaseMongoRepository(
    BaseRepositoryProtocol[Domain_T],
    Generic[Domain_T],
):
    domain_model: type[Domain_T]
    collection_name: str
    searchable_fields: tuple[str, ...]

    def __init__(self, database: Database[MongoDocument]):
        self.database = database
        self.collection = self.database[self.collection_name]

    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
    ) -> PaginatedResponse[Domain_T]:
        pagination = pagination or Pagination()
        skip = (pagination.page - 1) * pagination.limit

        pipeline = self._search_pipeline(search) + self._aggregation_pipeline()

        count_pipeline = [*pipeline, {"$count": "total"}]
        count_result = list(self.collection.aggregate(count_pipeline))
        total = count_result[0]["total"] if count_result else 0

        paginated_pipeline = [*pipeline, {"$skip": skip}, {"$limit": pagination.limit}]
        items_db = self.collection.aggregate(paginated_pipeline)
        items = [self._to_domain_entity(item) for item in items_db]

        return PaginatedResponse(total=total, limit=pagination.limit, items=items)

    def get_by_id(self, entity_id: EntityId, /) -> Domain_T | None:
        db_result = self._get_db_entity(ObjectId(str(entity_id)))

        return self._to_domain_entity(db_result) if db_result else None

    def create(self, entity: Domain_T, /) -> Domain_T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.insert_one(db_entity)
        db_result = self._get_db_entity(result.inserted_id)
        if not db_result:
            raise RuntimeError()

        return self._to_domain_entity(db_result)

    def update(self, entity: Domain_T, /) -> Domain_T:
        assert entity.id is not None
        entity_id = ObjectId(str(entity.id))

        db_entity = self._to_database_entity(entity)

        self.collection.replace_one({"_id": entity_id}, db_entity)
        db_result = self._get_db_entity(entity_id)
        if not db_result:
            raise RuntimeError()

        return self._to_domain_entity(db_result)

    def delete(self, entity: Domain_T, /) -> None:
        assert entity.id is not None
        entity_id = ObjectId(str(entity.id))

        self.collection.delete_one({"_id": entity_id})

    def _get_db_entity(self, entity_id: ObjectId, /) -> MongoDocument | None:
        pipeline = [
            {"$match": {"_id": ObjectId(str(entity_id))}},
            *self._aggregation_pipeline(),
        ]
        return next(self.collection.aggregate(pipeline), None)

    def _to_domain_entity(self, document: MongoDocument, /) -> Domain_T:
        document["id"] = str(document.pop("_id"))
        return self.domain_model.model_validate(document)

    @staticmethod
    def _to_database_entity(entity: Domain_T, /) -> MongoDocument:
        return entity.model_dump(exclude={"id"})

    def _search_pipeline(self, search: str | None) -> list[MongoDocument]:
        if not search:
            return []

        conditions = [
            {field: {"$regex": search, "$options": "i"}}
            for field in self.searchable_fields
        ]
        return [{"$match": {"$or": conditions}}]

    @staticmethod
    def _aggregation_pipeline() -> list[MongoDocument]:
        return []
