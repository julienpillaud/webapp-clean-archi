import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_domain
from app.api.pagination.dtos import PaginatedResponseDTO, PaginationDTO
from app.api.users.dtos import UserCreateDTO, UserDTO, UserUpdateDTO
from app.domain.domain import Domain

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginatedResponseDTO[UserDTO])
def get_users(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[PaginationDTO, Query()],
) -> Any:
    return domain.get_users(pagination=pagination.to_domain())


@router.get("/{user_id}", response_model=UserDTO)
def get_user(
    domain: Annotated[Domain, Depends(get_domain)],
    user_id: uuid.UUID,
) -> Any:
    return domain.get_user(user_id=user_id)


@router.post("", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    domain: Annotated[Domain, Depends(get_domain)],
    data: UserCreateDTO,
) -> Any:
    return domain.create_user(data=data.to_domain())


@router.patch("/{user_id}", response_model=UserDTO)
def update_user(
    domain: Annotated[Domain, Depends(get_domain)],
    user_id: uuid.UUID,
    data: UserUpdateDTO,
) -> Any:
    return domain.update_user(user_id=user_id, data=data.to_domain())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    domain: Annotated[Domain, Depends(get_domain)],
    user_id: uuid.UUID,
) -> None:
    domain.delete_user(user_id=user_id)
