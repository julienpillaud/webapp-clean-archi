from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_domain, get_filters
from app.api.utils import PaginatedResponseDTO
from app.domain.domain import Domain
from app.domain.entities import Pagination
from app.domain.filters import FilterEntity
from app.domain.items.entities import Item
from app.domain.items.repository import RepositoryType

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "",
    response_model=PaginatedResponseDTO[Item],
    dependencies=[Depends(get_current_user)],
)
def get_items(
    domain: Annotated[Domain, Depends(get_domain)],
    repository: RepositoryType,
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    search: str | None = None,
) -> Any:
    return domain.get_items(
        repository=repository,
        pagination=pagination,
        search=search,
        filters=filters,
    )


@router.post("/event")
def send_item_event(domain: Annotated[Domain, Depends(get_domain)]) -> dict[str, str]:
    domain.send_item_event()
    return {"detail": "Event sent successfully"}
