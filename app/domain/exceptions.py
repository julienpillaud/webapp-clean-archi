from app.domain.logger import logger


class DomainError(Exception):
    """Base class for domain exceptions."""

    def __init__(self, message: str) -> None:
        logger.error(message)
        super().__init__(message)


class BadRequestError(DomainError):
    """Domain error for a 400 HTTP status code."""


class ForbiddenError(DomainError):
    """Domain error for a 403 HTTP status code."""


class NotFoundError(DomainError):
    """Domain error for a 404 HTTP status code."""


class ConflictError(DomainError):
    """Domain error for a 409 HTTP status code."""


class UnprocessableContentError(DomainError):
    """Domain error for a 422 HTTP status code."""
