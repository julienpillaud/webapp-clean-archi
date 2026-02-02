from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_domain, get_filters
from app.api.users.dtos import UserDTO
from app.api.utils import PaginatedResponseDTO
from app.domain.domain import Domain
from app.domain.entities import Pagination
from app.domain.filters import FilterEntity

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    response_model=PaginatedResponseDTO[UserDTO],
    dependencies=[Depends(get_current_user)],
)
def get_users(
    domain: Annotated[Domain, Depends(get_domain)],
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    search: str | None = None,
) -> Any:
    return domain.get_users(pagination=pagination, search=search, filters=filters)
