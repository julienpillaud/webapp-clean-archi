from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

import typer
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty

from app.domain.exceptions import AlreadyExistsError, NotFoundError

P = ParamSpec("P")
R = TypeVar("R")


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


def print_result(result: Any, title: str, border_style: str = "none") -> None:
    print(Panel(Pretty(result), title=title, width=120, border_style=border_style))
