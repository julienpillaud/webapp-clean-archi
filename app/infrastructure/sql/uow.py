from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.uow import UnitOfWorkProtocol
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.sql.provider import SQLProvider


class SQLUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        self._session: Session | None = None
        SQLProvider.init(settings)
        self.session_factory = SQLProvider.get_session_factory()

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("No active session.")
        return self._session

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
