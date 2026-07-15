from typing import Annotated

from cleanstack import PaginatedResponse
from cleanstack.entities import EntityId, FilterEntity, Pagination, SortEntity
from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_domain,
    get_filters,
    get_sort_entities,
)
from app.core.domain.synchronous import Domain
from app.domain.posts.entities import Post, PostCreate, PostUpdate
from app.domain.posts.use_cases import (
    create_post,
    delete_post,
    get_post,
    get_posts,
    update_post,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def get_posts_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> PaginatedResponse[Post]:
    return domain.run(
        get_posts,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get("/{post_id}")
def get_post_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> Post:
    return domain.run(get_post, post_id=post_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PostCreate,
) -> Post:
    return domain.run(create_post, data=data)


@router.patch("/{post_id}")
def update_post_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
    data: PostUpdate,
) -> Post:
    return domain.run(update_post, post_id=post_id, data=data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> None:
    domain.run(delete_post, post_id=post_id)
