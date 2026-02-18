from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.mongo.base import MongoRepository


class ItemMongoRepository(MongoRepository[Item], ItemRepositoryProtocol):
    domain_model = Item
    collection_name = "items"
