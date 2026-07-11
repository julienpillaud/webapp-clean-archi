from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.sql.entities import OrmEntity
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.infrastructure.sql.logger import logger


class SQLResource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Engine
    session_factory: sessionmaker[Session]

    @classmethod
    def from_settings(cls, settings: Settings, /) -> SQLResource:
        engine = create_engine(
            url=str(settings.postgres_dsn),
            **settings.postgres_params,
        )
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("SQL engine up")
        return cls(
            engine=engine,
            session_factory=sessionmaker(bind=engine),
        )

    def start_transaction(self) -> Session:
        return self.session_factory()

    @staticmethod
    def end_transaction(
        session: Session | None,
        exc_val: BaseException | None,
        is_mutation: bool,
    ) -> None:
        # for protocol compliance
        if session is None:
            raise RuntimeError()

        if session.is_active:
            if exc_val is None and is_mutation:
                session.commit()
                logger.info("Transaction committed")
            else:
                session.rollback()
                logger.info("Transaction rollback")
        session.close()

    def release(self) -> None:
        logger.info("SQL engine released")
        self.engine.dispose()

    def reset(self) -> None:
        with self.session_factory() as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()


@contextmanager
def managed_session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
