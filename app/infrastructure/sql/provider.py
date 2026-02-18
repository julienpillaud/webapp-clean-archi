from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.infrastructure.sql.logger import logger


class SQLProvider:
    _engine: Engine | None = None
    _session_factory: sessionmaker[Session] | None = None

    @classmethod
    def init(cls, settings: Settings, /) -> None:
        if cls._engine is None:
            logger.debug("Initializing SQLAlchemy engine")
            cls._engine = create_engine(str(settings.postgres_dsn))
            cls._session_factory = sessionmaker(cls._engine)

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._engine is None:
            raise RuntimeError("Not initialized.")
        return cls._engine

    @classmethod
    def get_session_factory(cls) -> sessionmaker[Session]:
        if cls._session_factory is None:
            raise RuntimeError("Not initialized.")
        return cls._session_factory
