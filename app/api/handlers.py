# pyright: reportUnusedFunction=false
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import AlreadyExistsError, DomainError, NotFoundError


def add_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def api_exception_handler(
        request: Request, error: DomainError
    ) -> JSONResponse:
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
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )
