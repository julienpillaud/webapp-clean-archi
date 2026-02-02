from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_user, get_domain, get_filters
from app.api.posts.dtos import PostDTO
from app.api.utils import PaginatedResponseDTO
from app.domain.domain import Domain
from app.domain.entities import EntityId, Pagination
from app.domain.filters import FilterEntity
from app.domain.posts.entities import PostCreate, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "",
    response_model=PaginatedResponseDTO[PostDTO],
    dependencies=[Depends(get_current_user)],
)
def get_posts(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    search: str | None = None,
) -> Any:
    return domain.get_posts(pagination=pagination, search=search, filters=filters)


@router.get(
    "/{post_id}",
    response_model=PostDTO,
    dependencies=[Depends(get_current_user)],
)
def get_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> Any:
    return domain.get_post(post_id=post_id)


@router.post(
    "",
    response_model=PostDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_post(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PostCreate,
) -> Any:
    return domain.create_post(data=data)


@router.patch(
    "/{post_id}",
    response_model=PostDTO,
    dependencies=[Depends(get_current_user)],
)
def update_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
    data: PostUpdate,
) -> Any:
    return domain.update_post(post_id=post_id, data=data)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> None:
    domain.delete_post(post_id=post_id)
