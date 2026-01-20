from typing import Any

from faker import Faker
from sqlalchemy.orm import Session

from app.domain.entities import DomainEntity
from app.domain.interfaces.repository import RepositoryProtocol
from app.infrastructure.sql.base import OrmEntity, SqlRepository


class BaseFactory[T: DomainEntity]:
    repository: RepositoryProtocol[T]

    def build(self, **kwargs: Any) -> T:
        raise NotImplementedError()

    def create_one(self, **kwargs: Any) -> T:
        entity = self.build(**kwargs)
        created_entity = self.repository.create(entity)
        self._commit()
        return created_entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        return [self.create_one(**kwargs) for _ in range(count)]

    def _commit(self) -> None:
        raise NotImplementedError()


class BaseSqlFactory[DomainT: DomainEntity, OrmT: OrmEntity](BaseFactory[DomainT]):
    repository_class: type[SqlRepository[DomainT, OrmT]]

    def __init__(self, faker: Faker, session: Session):
        self.faker = faker
        self.session = session
        self.repository = self.repository_class(session=session)

    def _commit(self) -> None:
        self.session.commit()
