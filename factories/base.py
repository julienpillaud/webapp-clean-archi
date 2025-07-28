from typing import Any, Generic, TypeVar

from cleanstack.entities import DomainModel

T = TypeVar("T", bound=DomainModel)


class BaseFactory(Generic[T]):
    def create_one(self, **kwargs: Any) -> T:
        entity = self._build_entity(**kwargs)
        self._insert_one(entity)
        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self._build_entity(**kwargs) for _ in range(count)]
        self._insert_many(entities)
        return entities

    def _build_entity(self, **kwargs: Any) -> T:
        """Build a domain entity with the given kwargs."""
        raise NotImplementedError()

    def _insert_many(self, entities: list[T]) -> None:
        """Insert multiple entities into the database."""
        for entity in entities:
            self._insert_one(entity)

    def _insert_one(self, entity: T) -> None:
        """Insert a single entity into the database."""
        raise NotImplementedError()
