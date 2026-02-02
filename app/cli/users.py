from typing import Annotated

import typer
from pydantic import PositiveInt

from app.cli.utils import (
    get_domain_method,
    print_result,
)
from app.domain.entities import DEFAULT_PAGINATION_LIMIT, Pagination

app = typer.Typer()


@app.command()
def get_all(
    ctx: typer.Context,
    page: Annotated[PositiveInt, typer.Argument()] = 1,
    limit: Annotated[PositiveInt, typer.Argument()] = DEFAULT_PAGINATION_LIMIT,
) -> None:
    get_users = get_domain_method(ctx=ctx, method_name="get_users")
    users = get_users(pagination=Pagination(page=page, limit=limit))
    print_result(result=users, title="Users")
