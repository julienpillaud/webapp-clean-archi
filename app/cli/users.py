from typing import Annotated

import typer
from cleanstack.entities import EntityId
from pydantic import PositiveInt

from app.cli.utils import (
    get_domain_method,
    make_model_parser,
    parse_entity_id,
    print_result,
)
from app.domain.entities import DEFAULT_PAGINATION_LIMIT, Pagination
from app.domain.users.entities import UserCreate, UserUpdate

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


@app.command()
def get(
    ctx: typer.Context,
    user_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
) -> None:
    get_user = get_domain_method(ctx=ctx, method_name="get_user")
    user = get_user(user_id=user_id)
    print_result(result=user, title="User")


@app.command()
def create(
    ctx: typer.Context,
    data: Annotated[
        UserCreate,
        typer.Argument(parser=make_model_parser(UserCreate)),
    ],
) -> None:
    create_user = get_domain_method(ctx=ctx, method_name="create_user")
    user = create_user(data=data)
    print_result(result=user, title="User created", border_style="green")


@app.command()
def update(
    ctx: typer.Context,
    user_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
    data: Annotated[
        UserUpdate,
        typer.Argument(parser=make_model_parser(UserUpdate)),
    ],
) -> None:
    update_user = get_domain_method(ctx=ctx, method_name="update_user")
    user = update_user(user_id=user_id, data=data)
    print_result(result=user, title="User updated", border_style="green")


@app.command()
def delete(
    ctx: typer.Context,
    user_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
) -> None:
    delete_user = get_domain_method(ctx=ctx, method_name="delete_user")
    delete_user(user_id=user_id)
    print_result(result=None, title="User deleted", border_style="green")
