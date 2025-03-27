from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.domain.domain import UnitOfWorkProtocol


class SqlAlchemyUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        self.session_factory = sessionmaker(bind=engine)
        self._session = None

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("No active session")
        return self._session

    @contextmanager
    def transaction(self):
        self._session = self.session_factory()
        try:
            yield
        finally:
            self._session.close()
            self._session = None

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
