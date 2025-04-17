# pyright: reportUnusedFunction=false
import logging

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from app.domain.exceptions import AlreadyExistsError, DomainError, NotFoundError

logger = logging.getLogger(__name__)


def add_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def app_exception_handler(request: Request, error: DomainError) -> Response:
        if isinstance(error, NotFoundError):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": error.detail},
            )
        if isinstance(error, AlreadyExistsError):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": error.detail},
            )

        logger.error("Unhandled DomainError", exc_info=True)
        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )
