from cleanstack.sql.entities import OrmEntity
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.core.domain.synchronous import ResourceProtocol
from app.infrastructure.sql.logger import logger


class SQLEngine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Engine
    session_factory: sessionmaker[Session]

    @classmethod
    def from_settings(cls, settings: Settings, /) -> SQLEngine:
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

    def release(self) -> None:
        logger.info("SQL engine released")
        self.engine.dispose()

    def reset(self) -> None:
        with self.session_factory() as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()


class SQLResource(ResourceProtocol):
    def __init__(self, sql_engine: SQLEngine, /) -> None:
        self.session_factory = sql_engine.session_factory
        self.session: Session | None = None

    def start_transaction(self, transactional: bool) -> None:
        self.session = self.session_factory()

    def end_transaction(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        transactional: bool,
    ) -> None:
        if not self.session:
            return

        if self.session.is_active:
            if exc_type and exc_val:
                self.session.rollback()
                logger.info(f"Transaction rollback: {exc_type.__name__}({exc_val})")
            elif transactional:
                self.session.commit()
                logger.info("Transaction committed")

        self.session.close()
        self.session = None
