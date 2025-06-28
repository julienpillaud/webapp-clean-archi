from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_domain, get_settings
from app.core.config import Settings
from app.core.security import create_access_token
from app.domain.domain import Domain
from app.domain.entities import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/access-token")
async def get_access_token(
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = domain.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return create_access_token(settings=settings, subject=user.email)
