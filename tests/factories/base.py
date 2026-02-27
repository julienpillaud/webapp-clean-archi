from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from faker import Faker

from app.domain.entities import DomainEntity
from app.domain.interfaces.repository import RepositoryProtocol
from app.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from app.infrastructure.sql.uow import SQLContext, SQLUnitOfWork


class BaseFactory[T: DomainEntity](ABC):
    def create_one(self, **kwargs: Any) -> T:
        entity = self.build(**kwargs)
        with self._persistence_context():
            created = self._repository.create(entity)
            self._commit()
            return created

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self.build(**kwargs) for _ in range(count)]
        created_entities: list[T] = []
        with self._persistence_context():
            for entity in entities:
                created = self._repository.create(entity)
                created_entities.append(created)
            self._commit()
        return created_entities

    @abstractmethod
    def build(self, **kwargs: Any) -> T: ...

    @abstractmethod
    def _commit(self) -> None: ...

    @contextmanager
    @abstractmethod
    def _persistence_context(self) -> Iterator[None]: ...

    @property
    @abstractmethod
    def _repository(self) -> RepositoryProtocol[T]: ...


class BaseSQLFactory[T: DomainEntity](BaseFactory[T], ABC):
    def __init__(self, faker: Faker, context: SQLContext) -> None:
        self.faker = faker
        self.context = context
        self.uow = SQLUnitOfWork(context=context)

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.uow.transaction():
            yield

    def _commit(self) -> None:
        self.uow.commit()


class BaseMongoFactory[T: DomainEntity](BaseFactory[T], ABC):
    def __init__(self, faker: Faker, context: MongoContext) -> None:
        self.faker = faker
        self.uow = MongoUnitOfWork(context=context)

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.uow.transaction():
            yield

    def _commit(self) -> None:
        self.uow.commit()
