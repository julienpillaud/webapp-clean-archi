import re
import uuid
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

import typer
from pydantic import BaseModel, ValidationError
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty

from app.domain.entities import EntityId
from app.domain.exceptions import AlreadyExistsError, NotFoundError

P = ParamSpec("P")
R = TypeVar("R")

object_id_pattern = re.compile(r"^[a-fA-F0-9]{24}$")


def exception_handler(function: Callable[P, R]) -> Callable[P, R]:
    def decorator(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return function(*args, **kwargs)
        except NotFoundError as error:
            print_result(error, title="NotFoundError", border_style="yellow")
            raise typer.Exit(code=1) from error
        except AlreadyExistsError as error:
            print_result(error, title="AlreadyExistsError", border_style="yellow")
            raise typer.Exit(code=1) from error

    return decorator


def get_domain_method(ctx: typer.Context, method_name: str) -> Callable[..., Any]:
    domain = ctx.obj["domain"]
    return exception_handler(getattr(domain, method_name))


def make_model_parser(model: type[BaseModel]) -> Callable[[str], BaseModel]:
    def parser(value: str) -> BaseModel:
        try:
            return model.model_validate_json(value)
        except ValidationError as error:
            raise typer.BadParameter(
                f"Can't parse data to '{model.__name__}'"
            ) from error

    return parser


def parse_entity_id(value: str) -> EntityId:
    try:
        return uuid.UUID(value)
    except ValueError as error:
        raise typer.BadParameter("Must be UUID or ObjectId.") from error


def print_result(result: Any, title: str, border_style: str = "none") -> None:
    print(Panel(Pretty(result), title=title, width=120, border_style=border_style))
