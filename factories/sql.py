from typing import Generic, TypeVar

from cleanstack.entities import DomainModel
from sqlalchemy.orm import Session

from app.infrastructure.sql.models import OrmBase
from factories.base import BaseFactory

T = TypeVar("T", bound=DomainModel)
P = TypeVar("P", bound=OrmBase)


class SqlBaseFactory(BaseFactory[T], Generic[T, P]):
    def __init__(self, session: Session):
        self.session = session

    def _insert_one(self, entity: T) -> None:
        db_entity = self._to_database_entity(entity)
        self.session.add(db_entity)
        self.session.commit()

    def _to_database_entity(self, entity: T) -> P:
        """Must be implemented in subclasses for the Orm Entity"""
        raise NotImplementedError()
