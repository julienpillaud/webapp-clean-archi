import logging
from typing import Any, ClassVar

from sqlalchemy import delete, select
from sqlalchemy.orm import InstrumentedAttribute, Session
from sqlalchemy.orm.interfaces import ORMOption

from app.domain.entities import DomainEntity, EntityId, PaginatedResponse, Pagination
from app.domain.filters import FilterEntity
from app.domain.interfaces.repository import RepositoryProtocol
from app.infrastructure.sql.entities import OrmEntity
from app.infrastructure.sql.utils import SQLQueryBuilder

logger = logging.getLogger(__name__)


class SqlRepository[DomainT: DomainEntity, OrmT: OrmEntity](
    RepositoryProtocol[DomainT],
):
    domain_model: type[DomainT]
    orm_model: type[OrmT]
    select_options: tuple[ORMOption, ...] = ()
    filterable_fields: ClassVar[dict[str, InstrumentedAttribute[Any]]] = {}
    searchable_fields: tuple[InstrumentedAttribute[Any], ...] = ()

    def __init__(self, session: Session):
        self.session = session
        self.query_builder = SQLQueryBuilder(
            model=self.orm_model,
            select_options=self.select_options,
            filterable_fields=self.filterable_fields,
            searchable_fields=self.searchable_fields,
        )

    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
    ) -> PaginatedResponse[DomainT]:
        pagination = pagination or Pagination()

        queries = self.query_builder.build(
            search=search,
            filters=filters,
            pagination=pagination,
        )

        total = self.session.scalar(queries.count) or 0

        orm_entities = self.session.scalars(queries.data)
        items = [self._to_domain_entity(orm_entity) for orm_entity in orm_entities]

        return PaginatedResponse(total=total, limit=pagination.limit, items=items)

    def get_by_id(self, entity_id: EntityId) -> DomainT | None:
        db_result = self._get_db_entity(entity_id=entity_id)

        return self._to_domain_entity(db_result) if db_result else None

    def create(self, entity: DomainT, /) -> DomainT:
        orm_entity = self._to_database_entity(entity)

        self.session.add(orm_entity)
        self.session.flush()

        return self._to_domain_entity(orm_entity)

    def update(self, entity: DomainT, /) -> DomainT:
        db_entity = self._get_db_entity(entity_id=entity.id)
        if not db_entity:
            raise RuntimeError()

        for key, value in entity.model_dump(exclude={"id"}).items():
            if hasattr(db_entity, key):
                setattr(db_entity, key, value)

        return self._to_domain_entity(db_entity)

    def delete(self, entity: DomainT) -> None:
        stmt = delete(self.orm_model).where(self.orm_model.id == entity.id)
        self.session.execute(stmt)

    def _get_db_entity(self, entity_id: EntityId) -> OrmT | None:
        stmt = select(self.orm_model).where(self.orm_model.id == entity_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def _to_domain_entity(self, orm_entity: OrmT, /) -> DomainT:
        return self.domain_model.model_validate(orm_entity)

    def _to_database_entity(self, entity: DomainT, /) -> OrmT:
        return self.orm_model(**entity.model_dump())
