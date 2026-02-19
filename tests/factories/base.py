from typing import Any

from faker import Faker
from pymongo.database import Database
from sqlalchemy.orm import Session

from app.domain.entities import DomainEntity
from app.domain.interfaces.repository import RepositoryProtocol
from app.infrastructure.mongo.base import MongoDocument


class BaseFactory[T: DomainEntity]:
    def __init__(self, faker: Faker):
        self.faker = faker

    def build(self, **kwargs: Any) -> T:
        raise NotImplementedError()

    @property
    def repository(self) -> RepositoryProtocol[T]:
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


class BaseSQLFactory[T: DomainEntity](BaseFactory[T]):
    def __init__(self, faker: Faker, session: Session):
        super().__init__(faker)
        self.session = session

    def _commit(self) -> None:
        self.session.commit()


class BaseMongoFactory[T: DomainEntity](BaseFactory[T]):
    def __init__(self, faker: Faker, database: Database[MongoDocument]):
        super().__init__(faker)
        self.database = database

    def _commit(self) -> None:
        pass
