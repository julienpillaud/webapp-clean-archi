import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_domain
from app.api.dtos.pagination import PaginatedResponseDTO, PaginationDTO
from app.api.dtos.post import PostCreateDTO, PostDTO, PostUpdateDTO
from app.domain.domain import Domain

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PaginatedResponseDTO[PostDTO])
async def get_posts(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[PaginationDTO, Query()],
):
    return domain.get_posts(pagination=pagination.to_domain())


@router.get("/{post_id}", response_model=PostDTO)
async def get_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: uuid.UUID,
):
    return domain.get_post(post_id=post_id)


@router.post("", response_model=PostDTO, status_code=status.HTTP_201_CREATED)
async def create_post(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PostCreateDTO,
):
    return domain.create_post(data=data.to_domain())


@router.patch("/{post_id}", response_model=PostDTO)
async def update_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: uuid.UUID,
    data: PostUpdateDTO,
):
    return domain.update_post(post_id=post_id, data=data.to_domain())


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    domain: Annotated[Domain, Depends(get_domain)],
    post_id: uuid.UUID,
):
    domain.delete_post(post_id=post_id)
