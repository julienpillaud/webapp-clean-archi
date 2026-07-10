from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from cleanstack import BaseEntity
from sqlalchemy.orm import Session

from app.domain.interfaces.repository import RepositoryProtocol


class BaseSQLFactory[T: BaseEntity](ABC):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session_factory = session_factory
        self._session: Session | None = None

    def create_one(self, **kwargs: Any) -> T:  # noqa: ANN401
        entity = self.build(**kwargs)

        with self._persistence_context():
            self._repository.save(entity)

        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:  # noqa: ANN401
        entities = [self.build(**kwargs) for _ in range(count)]
        created_entities: list[T] = []

        with self._persistence_context():
            for entity in entities:
                self._repository.save(entity)
                created_entities.append(entity)

        return created_entities

    @abstractmethod
    def build(self, **kwargs: Any) -> T: ...  # noqa: ANN401

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.session_factory() as session:
            self._session = session
            yield
            session.commit()
        self._session = None

    @property
    @abstractmethod
    def _repository(self) -> RepositoryProtocol[T]: ...

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError()
        return self._session
