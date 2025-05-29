from typing import Any, Generic, TypeVar

from faker import Faker

from app.domain.entities import DomainModel

T = TypeVar("T", bound=DomainModel)
P = TypeVar("P")


class BaseFactory(Generic[T, P]):
    def __init__(self) -> None:
        self.faker = Faker()

    def create_one(self, **kwargs: Any) -> T:
        entity = self._build_entity(**kwargs)
        self._insert([entity])
        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self._build_entity(**kwargs) for _ in range(count)]
        self._insert(entities)
        return entities

    def _build_entity(self, **kwargs: Any) -> T:
        """Build a domain entity with the given kwargs."""
        raise NotImplementedError()

    def _insert(self, entities: list[T]) -> None:
        """Insert the entities into the database."""
        raise NotImplementedError()

    def _to_database_entity(self, entity: T) -> P:
        """Convert the domain entity to a database-compatible format."""
        raise NotImplementedError()
