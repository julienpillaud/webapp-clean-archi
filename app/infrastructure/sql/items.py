from cleanstack.sql import SyncSQLRepository

from app.domain.items.entities import Item
from app.infrastructure.sql.models import OrmItem


class ItemSQLRepository(SyncSQLRepository[Item, OrmItem]):
    domain_entity_type = Item
    orm_model_type = OrmItem
