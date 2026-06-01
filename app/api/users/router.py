from typing import Annotated, Any

from cleanstack.entities import FilterEntity, Pagination, SortEntity
from fastapi import APIRouter, Depends

from app.api.users.dtos import UserDTO
from app.api.utils import PaginatedResponseDTO
from app.core.context import Context
from app.dependencies.fastapi.dependencies import (
    get_context,
    get_current_user,
    get_filters,
    get_sort_entities,
)
from app.domain.users.commands import get_users_command

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    response_model=PaginatedResponseDTO[UserDTO],
    dependencies=[Depends(get_current_user)],
)
def get_users(
    context: Annotated[Context, Depends(get_context)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    search: str | None = None,
) -> Any:
    return get_users_command(
        context,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )
