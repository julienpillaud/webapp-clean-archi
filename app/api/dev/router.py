from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_domain
from app.domain.domain import Domain

router = APIRouter(tags=["dev"])


@router.get("/unexpected-error")
def simulate_unexpected_error(
    domain: Annotated[Domain, Depends(get_domain)],
):
    domain.unexpected_error()


@router.get("/unexpected-domain-error")
def simulate_unexpected_domain_error(
    domain: Annotated[Domain, Depends(get_domain)],
):
    domain.unexpected_domain_error()
