# pyright: reportUnusedFunction=false
import uuid
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dtos.pagination import PaginatedResponseDTO, PaginationDTO
from app.api.dtos.user import UserCreateDTO, UserDTO, UserUpdateDTO
from app.domain.domain import Domain


def user_router_factory(domain: Domain):
    router = APIRouter(prefix="/users", tags=["users"])

    @router.get("", response_model=PaginatedResponseDTO[UserDTO])
    async def get_users(pagination: Annotated[PaginationDTO, Query()]):
        return domain.get_users(pagination=pagination.to_domain())

    @router.get("/{user_id}", response_model=UserDTO)
    async def get_user(user_id: uuid.UUID):
        return domain.get_user(user_id=user_id)

    @router.post("", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
    async def create_user(data: UserCreateDTO):
        return domain.create_user(data=data.to_domain())

    @router.patch("/{user_id}", response_model=UserDTO)
    async def update_user(user_id: uuid.UUID, data: UserUpdateDTO):
        return domain.update_user(user_id=user_id, data=data.to_domain())

    @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(user_id: uuid.UUID):
        domain.delete_user(user_id=user_id)

    return router
