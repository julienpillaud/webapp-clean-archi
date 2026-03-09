from cleanstack.infrastructure.sql.base import SQLRepository

from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.models import OrmItem


class ItemSQLRepository(SQLRepository[Item, OrmItem], ItemRepositoryProtocol):
    domain_entity_type = Item
    orm_model_type = OrmItem
