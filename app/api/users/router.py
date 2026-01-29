from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_domain, get_filters
from app.api.users.dtos import UserDTO
from app.api.utils import PaginatedResponseDTO
from app.domain.domain import Domain
from app.domain.entities import EntityId, Pagination
from app.domain.filters import FilterEntity
from app.domain.users.entities import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginatedResponseDTO[UserDTO])
def get_users(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    search: str | None = None,
) -> Any:
    return domain.get_users(pagination=pagination, search=search, filters=filters)


@router.get("/{user_id}", response_model=UserDTO)
def get_user(
    domain: Annotated[Domain, Depends(get_domain)],
    user_id: EntityId,
) -> Any:
    return domain.get_user(user_id=user_id)


@router.post("", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    domain: Annotated[Domain, Depends(get_domain)],
    data: UserCreate,
) -> Any:
    return domain.create_user(data=data)


@router.patch("/{user_id}", response_model=UserDTO)
def update_user(
    domain: Annotated[Domain, Depends(get_domain)],
    user_id: EntityId,
    data: UserUpdate,
) -> Any:
    return domain.update_user(user_id=user_id, data=data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    domain: Annotated[Domain, Depends(get_domain)],
    user_id: EntityId,
) -> None:
    domain.delete_user(user_id=user_id)
