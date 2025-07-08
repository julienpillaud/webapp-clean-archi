import logging
from typing import Generic, TypeVar

from sqlalchemy import Select, delete, func, or_, select
from sqlalchemy.orm import InstrumentedAttribute, Session
from sqlalchemy.orm.interfaces import ORMOption

from app.domain.entities import DomainModel, EntityId, PaginatedResponse, Pagination
from app.domain.interfaces.repository import BaseRepositoryProtocol
from app.infrastructure.sql.models import OrmBase

logger = logging.getLogger(__name__)

Domain_T = TypeVar("Domain_T", bound=DomainModel)
Orm_T = TypeVar("Orm_T", bound=OrmBase)


class BaseSqlRepository(BaseRepositoryProtocol[Domain_T], Generic[Domain_T, Orm_T]):
    domain_model: type[Domain_T]
    orm_model: type[Orm_T]
    searchable_fields: tuple[InstrumentedAttribute[str], ...]
    select_options: tuple[ORMOption, ...] = ()

    def __init__(self, session: Session):
        logger.debug(f"Instantiate '{self.__class__.__name__}'")
        self.session = session

    def get_all(
        self,
        pagination: Pagination | None = None,
        search: str | None = None,
    ) -> PaginatedResponse[Domain_T]:
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

    def get_by_id(self, entity_id: EntityId) -> Domain_T | None:
        db_result = self._get_db_entity(entity_id=entity_id)

        return self._to_domain_entity(db_result) if db_result else None

    def create(self, entity: Domain_T, /) -> Domain_T:
        orm_entity = self._to_database_entity(entity)

        self.session.add(orm_entity)
        self.session.flush()

        return self._to_domain_entity(orm_entity)

    def update(self, entity: Domain_T, /) -> Domain_T:
        db_entity = self._get_db_entity(entity_id=entity.id)
        if not db_entity:
            raise RuntimeError()

        for key, value in entity.model_dump(exclude={"id"}).items():
            if hasattr(db_entity, key):
                setattr(db_entity, key, value)

        return self._to_domain_entity(db_entity)

    def delete(self, entity: Domain_T) -> None:
        stmt = delete(self.orm_model).where(self.orm_model.id == entity.id)
        self.session.execute(stmt)

    def _get_db_entity(self, entity_id: EntityId) -> Orm_T | None:
        stmt = select(self.orm_model).where(self.orm_model.id == entity_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def _to_domain_entity(self, orm_entity: Orm_T, /) -> Domain_T:
        return self.domain_model.model_validate(orm_entity)

    def _to_database_entity(self, entity: Domain_T, /) -> Orm_T:
        return self.orm_model(**entity.model_dump())

    def _apply_search(
        self, stmt: Select[tuple[Orm_T]], search: str | None
    ) -> Select[tuple[Orm_T]]:
        if not search:
            return stmt

        conditions = [field.ilike(f"%{search}%") for field in self.searchable_fields]
        return stmt.where(or_(*conditions))

    def _total_count(self, stmt: Select[tuple[Orm_T]]) -> int:
        count_stmt = stmt.with_only_columns(func.count()).select_from(self.orm_model)
        return self.session.scalar(count_stmt) or 0

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[Orm_T]], pagination: Pagination
    ) -> Select[tuple[Orm_T]]:
        offset = (pagination.page - 1) * pagination.limit
        return stmt.offset(offset).limit(pagination.limit)
