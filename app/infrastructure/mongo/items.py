from cleanstack.infrastructure.mongo.base import MongoRepository

from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol


class ItemMongoRepository(MongoRepository[Item], ItemRepositoryProtocol):
    domain_entity_type = Item
    collection_name = "items"
