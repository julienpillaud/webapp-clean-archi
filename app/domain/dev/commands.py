from cleanstack.exceptions import DomainError

from app.domain.context import ContextProtocol
from app.domain.exceptions import CustomError


class UnexpectedError(Exception):
    pass


class UnexpectedDomainError(DomainError):
    pass


def benchmark_command(context: ContextProtocol) -> str:
    return ""


def custom_error_command(context: ContextProtocol) -> None:
    raise CustomError("Custom error")


def unexpected_error_command(context: ContextProtocol) -> None:
    raise UnexpectedError("Unexpected error")


def unexpected_domain_error_command(context: ContextProtocol) -> None:
    raise UnexpectedDomainError("Unexpected domain error")
