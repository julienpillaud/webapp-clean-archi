import uuid
from typing import Generic, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.domain.entities import DomainModel, PaginatedResponse, Pagination
from app.domain.exceptions import NotFoundError
from app.domain.interfaces.repository import BaseRepositoryProtocol
from app.infrastructure.repository.models import OrmBase

Domain_T = TypeVar("Domain_T", bound=DomainModel)
Orm_T = TypeVar("Orm_T", bound=OrmBase)


class BaseSqlRepository(BaseRepositoryProtocol[Domain_T], Generic[Domain_T, Orm_T]):
    domain_model: type[Domain_T]
    orm_model: type[Orm_T]

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self, pagination: Pagination | None = None
    ) -> PaginatedResponse[Domain_T]:
        count_stmt = select(func.count()).select_from(self.orm_model)
        total = self.session.scalar(count_stmt) or 0

        pagination = pagination or Pagination()
        stmt = select(self.orm_model)
        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        orm_entities = self.session.scalars(stmt)
        items = [
            self.orm_to_domain_entity(orm_entity=orm_entity)
            for orm_entity in orm_entities
        ]

        return PaginatedResponse(total=total, limit=pagination.limit, items=items)

    def get_by_id(self, entity_id: uuid.UUID) -> Domain_T | None:
        orm_entity = self._get_entity_by_id(entity_id=entity_id)
        return self.orm_to_domain_entity(orm_entity=orm_entity) if orm_entity else None

    def create(self, entity: Domain_T, /):
        orm_entity = self.domain_to_orm_entity(entity=entity)
        self.session.add(orm_entity)

    def update(self, entity: Domain_T, /):
        orm_entity = self._get_entity_by_id(entity_id=entity.id)
        if not orm_entity:
            raise NotFoundError("Entity not found")

        for key, value in entity.model_dump().items():
            if hasattr(orm_entity, key):
                setattr(orm_entity, key, value)

    def delete(self, entity_id: uuid.UUID):
        orm_entity = self._get_entity_by_id(entity_id=entity_id)
        self.session.delete(orm_entity)

    def _get_entity_by_id(self, entity_id: uuid.UUID) -> Orm_T | None:
        stmt = select(self.orm_model).where(self.orm_model.id == entity_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def orm_to_domain_entity(self, orm_entity: Orm_T) -> Domain_T:
        return self.domain_model.model_validate(orm_entity)

    def domain_to_orm_entity(self, entity: Domain_T) -> Orm_T:
        return self.orm_model(**entity.model_dump())

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[Orm_T]], pagination: Pagination
    ) -> Select[tuple[Orm_T]]:
        offset = (pagination.page - 1) * pagination.limit
        return stmt.offset(offset).limit(pagination.limit)
