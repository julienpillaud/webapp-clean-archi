from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.base import SQLRepository
from app.infrastructure.sql.models import OrmItem


class ItemSQLRepository(SQLRepository[Item, OrmItem], ItemRepositoryProtocol):
    domain_model = Item
    orm_model = OrmItem
