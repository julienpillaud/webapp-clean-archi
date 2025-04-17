from app.domain.context import ContextProtocol
from app.domain.exceptions import DomainError


class UnexpectedError(Exception):
    pass


class UnexpectedDomainError(DomainError):
    pass


def unexpected_error_command(context: ContextProtocol) -> None:
    raise UnexpectedError("Unexpected error")


def unexpected_domain_error_command(context: ContextProtocol) -> None:
    raise UnexpectedDomainError("Unexpected domain error")
