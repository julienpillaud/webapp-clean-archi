import uuid

from cleanstack.infrastructure.sql.uow import SQLContext
from sqlalchemy import select

from app.core.config import Settings
from app.core.logger import logger
from app.infrastructure.sql.entities import OrmEntity
from app.infrastructure.sql.models import OrmUser


def initialize_app(settings: Settings) -> None:
    initialize_sql_database(settings=settings)


def initialize_sql_database(settings: Settings) -> None:
    """Only used in this project for convenience."""
    logger.info("Creating SQL database tables")
    context = SQLContext.from_settings(url=str(settings.postgres_dsn))
    session_factory = context.session_factory
    OrmEntity.metadata.create_all(context.engine)

    provider_id = uuid.UUID("019c7037-f5bf-7305-b68a-510430df2d3c")
    with session_factory() as session:
        stmt = select(OrmUser).where(OrmUser.provider_id == str(provider_id))
        user = session.execute(stmt).scalar_one_or_none()
        if not user:
            logger.debug("Creating dev user")
            user = OrmUser(
                id=uuid.uuid7(),
                provider_id=str(provider_id),
                email="user@mail.com",
                username="user",
            )
            session.add(user)
            session.commit()
