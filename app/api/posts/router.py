from typing import Annotated

from cleanstack import PaginatedResponse
from cleanstack.entities import EntityId, FilterEntity, Pagination, SortEntity
from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_domain, get_filters, get_sort_entities
from app.core.domain import Domain
from app.domain.posts.commands import (
    create_post_command,
    delete_post_command,
    get_post_command,
    get_posts_command,
    update_post_command,
)
from app.domain.posts.entities import Post, PostCreate, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def get_posts(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> PaginatedResponse[Post]:
    return domain.run(
        get_posts_command,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get("/{post_id}")
def get_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> Post:
    return domain.run(get_post_command, post_id=post_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PostCreate,
) -> Post:
    return domain.run(create_post_command, data=data)


@router.patch("/{post_id}")
def update_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
    data: PostUpdate,
) -> Post:
    return domain.run(update_post_command, post_id=post_id, data=data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> None:
    domain.run(delete_post_command, post_id=post_id)
