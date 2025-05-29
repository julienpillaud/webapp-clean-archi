from app.domain.generics.entities import GenericEntity
from app.domain.generics.repository import GenericEntityRepositoryProtocol
from app.infrastructure.mongo.base import BaseMongoRepository


class GenericEntityMongoRepository(
    BaseMongoRepository[GenericEntity],
    GenericEntityRepositoryProtocol,
):
    domain_model = GenericEntity
    collection_name = "generics"
