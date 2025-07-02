from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_domain
from app.api.users.dtos import UserDTO
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter(tags=["dev"])


@router.get("/protected", response_model=UserDTO)
def protected_route(
    current_user: Annotated[User, Depends(get_current_user)],
) -> Any:
    return current_user


@router.get("/unexpected-error")
def simulate_unexpected_error(
    domain: Annotated[Domain, Depends(get_domain)],
) -> None:
    domain.unexpected_error()


@router.get("/unexpected-domain-error")
def simulate_unexpected_domain_error(
    domain: Annotated[Domain, Depends(get_domain)],
) -> None:
    domain.unexpected_domain_error()
