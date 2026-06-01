from typing import Annotated, Any

from cleanstack.entities import EntityId, FilterEntity, Pagination, SortEntity
from fastapi import APIRouter, Depends, status

from app.api.posts.dtos import PostDTO
from app.api.utils import PaginatedResponseDTO
from app.core.context import Context
from app.dependencies.fastapi.dependencies import (
    get_context,
    get_current_user,
    get_filters,
    get_sort_entities,
)
from app.domain.posts.commands import (
    create_post_command,
    delete_post_command,
    get_post_command,
    get_posts_command,
    update_post_command,
)
from app.domain.posts.entities import PostCreate, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "",
    response_model=PaginatedResponseDTO[PostDTO],
    dependencies=[Depends(get_current_user)],
)
def get_posts(
    context: Annotated[Context, Depends(get_context)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> Any:
    return get_posts_command(
        context,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get(
    "/{post_id}",
    response_model=PostDTO,
    dependencies=[Depends(get_current_user)],
)
def get_post(
    context: Annotated[Context, Depends(get_context)],
    post_id: EntityId,
) -> Any:
    return get_post_command(context, post_id=post_id)


@router.post(
    "",
    response_model=PostDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_post(
    context: Annotated[Context, Depends(get_context)],
    data: PostCreate,
) -> Any:
    return create_post_command(context, data=data)


@router.patch(
    "/{post_id}",
    response_model=PostDTO,
    dependencies=[Depends(get_current_user)],
)
def update_post(
    context: Annotated[Context, Depends(get_context)],
    post_id: EntityId,
    data: PostUpdate,
) -> Any:
    return update_post_command(context, post_id=post_id, data=data)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_post(
    context: Annotated[Context, Depends(get_context)],
    post_id: EntityId,
) -> None:
    delete_post_command(context, post_id=post_id)
