from typing import Annotated

import typer
from pydantic import PositiveInt

from app.cli.utils import (
    get_domain_method,
    make_model_parser,
    parse_entity_id,
    print_result,
)
from app.domain.entities import DEFAULT_PAGINATION_LIMIT, EntityId, Pagination
from app.domain.posts.entities import PostCreate, PostUpdate

app = typer.Typer()


@app.command()
def get_all(
    ctx: typer.Context,
    page: Annotated[PositiveInt, typer.Argument()] = 1,
    limit: Annotated[PositiveInt, typer.Argument()] = DEFAULT_PAGINATION_LIMIT,
) -> None:
    get_posts = get_domain_method(ctx=ctx, method_name="get_posts")
    posts = get_posts(pagination=Pagination(page=page, limit=limit))
    print_result(result=posts, title="Posts")


@app.command()
def get(
    ctx: typer.Context,
    post_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
) -> None:
    get_post = get_domain_method(ctx=ctx, method_name="get_post")
    post = get_post(post_id=post_id)
    print_result(result=post, title="Post")


@app.command()
def create(
    ctx: typer.Context,
    data: Annotated[
        PostCreate,
        typer.Argument(parser=make_model_parser(PostCreate)),
    ],
) -> None:
    create_post = get_domain_method(ctx=ctx, method_name="create_post")
    post = create_post(data=data)
    print_result(result=post, title="Post created", border_style="green")


@app.command()
def update(
    ctx: typer.Context,
    post_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
    data: Annotated[
        PostUpdate,
        typer.Argument(parser=make_model_parser(PostUpdate)),
    ],
) -> None:
    update_post = get_domain_method(ctx=ctx, method_name="update_post")
    post = update_post(post_id=post_id, data=data)
    print_result(result=post, title="Post updated", border_style="green")


@app.command()
def delete(
    ctx: typer.Context,
    post_id: Annotated[EntityId, typer.Argument(parser=parse_entity_id)],
) -> None:
    delete_post = get_domain_method(ctx=ctx, method_name="delete_post")
    delete_post(post_id=post_id)
    print_result(result=None, title="Post deleted", border_style="green")
