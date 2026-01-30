import logging
from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache

import logfire
from cleanstack.domain import UnitOfWorkProtocol
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.domain.context import ContextProtocol
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.dummies import DummySqlRepository
from app.infrastructure.sql.posts import PostSqlRepository
from app.infrastructure.sql.users import UserSqlRepository

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_engine(settings: Settings) -> Engine:
    engine = create_engine(str(settings.postgres_dsn))
    logger.debug(f"Created engine {engine.url.render_as_string(hide_password=True)}")
    logfire.instrument_sqlalchemy(engine=engine)
    return engine


@lru_cache(maxsize=1)
def get_session_factory(settings: Settings) -> sessionmaker[Session]:
    engine = get_engine(settings=settings)
    return sessionmaker(bind=engine)


class SQLUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings) -> None:
        self._session: Session | None = None
        self.settings = settings
        self._session_factory = get_session_factory(settings=settings)

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


class SQLContext(SQLUnitOfWork, ContextProtocol):
    @property
    def dummy_repository(self) -> DummyRepositoryProtocol:
        return DummySqlRepository(session=self.session)

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSqlRepository(session=self.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSqlRepository(session=self.session)
