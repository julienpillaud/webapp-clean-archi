from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.uow import UnitOfWorkProtocol
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.sql.logger import logger


class SQLContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Engine
    session_factory: sessionmaker[Session]

    @classmethod
    def from_settings(cls, dsn: str) -> SQLContext:
        logger.info(f"Creating SQLAlchemy engine: {dsn}")
        engine = create_engine(dsn)
        session_factory = sessionmaker(engine)
        return cls(engine=engine, session_factory=session_factory)


class SQLUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, context: SQLContext) -> None:
        self._session: Session | None = None
        self._session_factory = context.session_factory

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("No active session.")
        return self._session

    @contextmanager
    def transaction(self) -> Iterator[None]:
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
