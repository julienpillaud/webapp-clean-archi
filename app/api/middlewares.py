import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from app.core.logger import logger


def add_timing_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def timing_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.perf_counter()
        try:
            return await call_next(request)
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"Use case [{elapsed:.1f} ms]")
