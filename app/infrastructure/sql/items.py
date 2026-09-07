from cleanstack import FilterEntity, PaginatedResponse, Pagination, SortEntity
from cleanstack.sql import SyncSQLRepository
from sqlalchemy.orm import Session

from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.models import OrmItem


class ItemSQLRepository(ItemRepositoryProtocol):
    domain_entity_type = Item
    orm_model_type = OrmItem
    searchable_fields = ()

    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = SyncSQLRepository[Item, OrmItem].from_binding(
            binding=self,
            session=session,
        )

    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Item]:
        return self.repository.get_all(
            search=search,
            filters=filters,
            sort=sort,
            pagination=pagination,
        )

    def save(self, entity: Item, /) -> None:
        self.repository.save(entity)
