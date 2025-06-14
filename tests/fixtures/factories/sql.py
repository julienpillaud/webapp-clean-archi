from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.domain.entities import DomainModel
from app.infrastructure.sql.models import OrmBase
from tests.fixtures.factories.base import BaseFactory

T = TypeVar("T", bound=DomainModel)
P = TypeVar("P", bound=OrmBase)


class SqlBaseFactory(BaseFactory[T], Generic[T, P]):
    def __init__(self, session: Session):
        self.session = session

    def _insert(self, entities: list[T]) -> None:
        for entity in entities:
            db_entity = self._to_database_entity(entity)
            self.session.add(db_entity)
            self.session.commit()
            entity.id = db_entity.id

    def _to_database_entity(self, entity: T) -> P:
        raise NotImplementedError()
