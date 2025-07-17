import logging
from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache

import logfire
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.domain.interfaces.task_queue import TaskQueueProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.celery_task_queue.celery_task_queue import CeleryTaskQueue
from app.infrastructure.sql.posts import PostSqlRepository
from app.infrastructure.sql.users import UserSqlRepository

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_engine(settings: Settings) -> Engine:
    logger.info(f"Creating engine {settings.postgres_dsn}")
    engine = create_engine(str(settings.postgres_dsn))
    logfire.instrument_sqlalchemy(engine=engine)
    return engine


class SqlContext(TransactionalContextProtocol):
    def __init__(self, settings: Settings) -> None:
        logger.info("Creating Sql context")
        engine = get_engine(settings=settings)
        self._session_factory = sessionmaker(engine)
        self._session: Session | None = None

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

    @property
    def task_queue(self) -> TaskQueueProtocol:
        return CeleryTaskQueue()
