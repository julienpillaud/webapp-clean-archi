from cleanstack.sql.entities import OrmEntity
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.core.domain.synchronous import TransactionProtocol
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

    def release(self) -> None:
        logger.info("SQL engine released")
        self.engine.dispose()

    def reset(self) -> None:
        with self.session_factory() as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()


class SQLTransaction(TransactionProtocol):
    def __init__(self, resource: SQLResource, /) -> None:
        self.resource = resource
        self.session: Session | None = None

    def start(self) -> None:
        self.session = self.resource.session_factory()

    def end(self, error: BaseException | None) -> None:
        if not self.session:
            return

        if self.session.is_active:
            if error:
                self.session.rollback()
                logger.warning(f"Transaction rollback: {type(error).__name__}({error})")
            else:
                self.session.commit()
                logger.info("Transaction committed")

        self.session.close()
        self.session = None
