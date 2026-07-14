from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.api.logger import logger
from app.core.config import Settings
from app.infrastructure.sql.resource import SQLEngine


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.sql_engine = SQLEngine.from_settings(settings)
        logger.info("Application startup complete")

        yield

        app.state.sql_engine.release()
        logger.info("Application shutdown complete")

    return lifespan
