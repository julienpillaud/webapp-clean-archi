from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.api.logger import logger
from app.core.config import Settings
from app.infrastructure.sql.utils import SQLResource


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.sql_resource = SQLResource.from_settings(settings)
        logger.info("Application startup complete")

        yield

        app.state.sql_resource.release()
        logger.info("Application shutdown complete")

    return lifespan
