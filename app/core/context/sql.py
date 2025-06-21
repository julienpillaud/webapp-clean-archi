from collections.abc import Iterator
from contextlib import contextmanager

import logfire
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.posts import PostSqlRepository
from app.infrastructure.sql.users import UserSqlRepository


class SqlContext(TransactionalContextProtocol):
    _session_factory: sessionmaker[Session] | None = None
    _session: Session | None = None

    @classmethod
    def initialize(cls, settings: Settings) -> None:
        engine = create_engine(str(settings.sqlalchemy_uri))
        cls._session_factory = sessionmaker(bind=engine)
        logfire.instrument_sqlalchemy(engine=engine)

    @contextmanager
    def transaction(self) -> Iterator[None]:
        if not self._session_factory:
            raise RuntimeError("Session factory not initialized.")

        self._session = self._session_factory()
        try:
            yield
        finally:
            self._session.close()
            self._session = None

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("No active session.")
        return self._session

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSqlRepository(session=self.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSqlRepository(session=self.session)
