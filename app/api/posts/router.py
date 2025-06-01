from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_domain
from app.api.pagination.dtos import PaginatedResponseDTO, PaginationDTO
from app.api.posts.dtos import PostCreateDTO, PostDTO, PostUpdateDTO
from app.domain.domain import Domain
from app.domain.entities import EntityId

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PaginatedResponseDTO[PostDTO])
def get_posts(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[PaginationDTO, Query()],
) -> Any:
    return domain.get_posts(pagination=pagination.to_domain())


@router.get("/{post_id}", response_model=PostDTO)
def get_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> Any:
    return domain.get_post(post_id=post_id)


@router.post("", response_model=PostDTO, status_code=status.HTTP_201_CREATED)
def create_post(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PostCreateDTO,
) -> Any:
    return domain.create_post(data=data.to_domain())


@router.patch("/{post_id}", response_model=PostDTO)
def update_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
    data: PostUpdateDTO,
) -> Any:
    return domain.update_post(post_id=post_id, data=data.to_domain())


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: EntityId,
) -> None:
    domain.delete_post(post_id=post_id)
