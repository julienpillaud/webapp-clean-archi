from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.api.logger import logger
from app.core.config import Settings
from app.infrastructure.sql.utils import create_sql_resource


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        sql_resource = create_sql_resource(settings=settings)
        app.state.sql_engine = sql_resource.engine
        app.state.sql_session_factory = sql_resource.session_factory

        yield

        sql_resource.release()
        logger.info("Application shutdown complete")

    return lifespan
