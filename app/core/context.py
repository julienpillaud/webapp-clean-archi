from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.domain.posts.repository import PostRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.repository.post import PostSqlRepository
from app.infrastructure.repository.user import UserSqlRepository


class Context(TransactionalContextProtocol):
    def __init__(self, settings: Settings):
        engine = create_engine(str(settings.sqlalchemy_database_uri))
        self.session_factory = sessionmaker(bind=engine)
        self._session: Session | None = None

    @contextmanager
    def transaction(self) -> Iterator[None]:
        self._session = self.session_factory()
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
            raise RuntimeError("No active session")
        return self._session

    @property
    def post_repository(self) -> PostRepositoryProtocol:
        return PostSqlRepository(session=self.session)

    @property
    def user_repository(self) -> UserRepositoryProtocol:
        return UserSqlRepository(session=self.session)
