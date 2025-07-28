from typing import Annotated, Any

from cleanstack.entities import EntityId
from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_domain
from app.api.posts.dtos import PostDTO
from app.api.utils import BaseQuery, PaginatedResponseDTO
from app.domain.domain import Domain
from app.domain.posts.entities import PostCreate, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PaginatedResponseDTO[PostDTO])
def get_posts(
    domain: Annotated[Domain, Depends(get_domain)],
    query: Annotated[BaseQuery, Query()],
) -> Any:
    return domain.get_posts(pagination=query.pagination, search=query.search)


@router.get("/{post_id}", response_model=PostDTO)
def get_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> Any:
    return domain.get_post(post_id=post_id)


@router.post("", response_model=PostDTO, status_code=status.HTTP_201_CREATED)
def create_post(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PostCreate,
) -> Any:
    return domain.create_post(data=data)


@router.patch("/{post_id}", response_model=PostDTO)
def update_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
    data: PostUpdate,
) -> Any:
    return domain.update_post(post_id=post_id, data=data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> None:
    domain.delete_post(post_id=post_id)
