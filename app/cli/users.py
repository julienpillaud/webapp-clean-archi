import uuid
from typing import Annotated

import typer
from pydantic import ValidationError
from rich import print

from app.cli.utils import exception_handler, print_result
from app.domain.entities import EntityId, Pagination
from app.domain.users.entities import UserCreate

app = typer.Typer()


def parse_user_create(value: str) -> UserCreate:
    try:
        return UserCreate.model_validate_json(value)
    except ValidationError as error:
        print(f"[red]Error parsing UserCreate data: {error}[/red]")
        raise typer.Exit(code=1) from error


def parse_entity_id(value: str) -> EntityId:
    try:
        return uuid.UUID(value)
    except ValueError:
        return value


@app.command()
def get_all(ctx: typer.Context) -> None:
    domain = ctx.obj["domain"]
    get_users = exception_handler(domain.get_users)
    users = get_users(Pagination())
    print_result(result=users, title="Users")


@app.command()
def get(
    ctx: typer.Context,
    user_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
) -> None:
    domain = ctx.obj["domain"]
    get_user = exception_handler(domain.get_user)
    user = get_user(user_id=user_id)
    print_result(result=user, title="User")


@app.command()
def create(
    ctx: typer.Context,
    data: Annotated[UserCreate, typer.Argument(parser=parse_user_create)],
) -> None:
    domain = ctx.obj["domain"]
    create_user = exception_handler(domain.create_user)
    user = create_user(data=data)
    print_result(result=user, title="User created", border_style="green")
