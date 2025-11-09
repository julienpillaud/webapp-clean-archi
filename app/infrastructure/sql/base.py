import logging

from cleanstack.entities import DomainModel, EntityId
from cleanstack.infrastructure.sql.entities import OrmBase
from sqlalchemy import Select, delete, func, or_, select
from sqlalchemy.orm import InstrumentedAttribute, Session
from sqlalchemy.orm.interfaces import ORMOption

from app.domain.entities import PaginatedResponse, Pagination
from app.domain.interfaces.repository import BaseRepositoryProtocol

logger = logging.getLogger(__name__)


class BaseSqlRepository[DomainT: DomainModel, OrmT: OrmBase](
    BaseRepositoryProtocol[DomainT],
):
    domain_model: type[DomainT]
    orm_model: type[OrmT]
    searchable_fields: tuple[InstrumentedAttribute[str], ...]
    select_options: tuple[ORMOption, ...] = ()

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
    ) -> PaginatedResponse[DomainT]:
        pagination = pagination or Pagination()

        stmt = select(self.orm_model)
        if self.select_options:
            stmt = stmt.options(*self.select_options)

        stmt = self._apply_search(stmt=stmt, search=search)
        total = self._total_count(stmt=stmt)
        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        orm_entities = self.session.scalars(stmt)
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

    def _apply_search(
        self, stmt: Select[tuple[OrmT]], search: str | None
    ) -> Select[tuple[OrmT]]:
        if not search:
            return stmt

        conditions = [field.ilike(f"%{search}%") for field in self.searchable_fields]
        return stmt.where(or_(*conditions))

    def _total_count(self, stmt: Select[tuple[OrmT]]) -> int:
        count_stmt = stmt.with_only_columns(func.count()).select_from(self.orm_model)
        return self.session.scalar(count_stmt) or 0

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[OrmT]], pagination: Pagination
    ) -> Select[tuple[OrmT]]:
        offset = (pagination.page - 1) * pagination.limit
        return stmt.offset(offset).limit(pagination.limit)
