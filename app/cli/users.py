from typing import Annotated

import typer
from cleanstack.entities import DEFAULT_PAGINATION_SIZE, Pagination
from pydantic import PositiveInt

from app.cli.utils import (
    get_domain_method,
    print_result,
)

app = typer.Typer()


@app.command()
def get_all(
    ctx: typer.Context,
    page: Annotated[PositiveInt, typer.Argument()] = 1,
    limit: Annotated[PositiveInt, typer.Argument()] = DEFAULT_PAGINATION_SIZE,
) -> None:
    get_users = get_domain_method(ctx=ctx, method_name="get_users")
    users = get_users(pagination=Pagination(page=page, limit=limit))
    print_result(result=users, title="Users")
