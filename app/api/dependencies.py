import uuid
from functools import lru_cache
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.core.config import Settings
from app.core.context.utils import get_context
from app.domain.domain import Domain, TransactionalContextProtocol
from app.domain.users.entities import User

oauth2_password_bearer = OAuth2PasswordBearer(tokenUrl="auth/access-token")

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_domain(
    context: Annotated[TransactionalContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)


async def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    token: Annotated[str, Depends(oauth2_password_bearer)],
) -> User:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except InvalidTokenError as error:
        raise credential_exception from error

    user_id = payload.get("sub")
    if user_id is None:
        raise credential_exception

    user = domain.get_user(user_id=uuid.UUID(user_id))
    if user is None:
        raise credential_exception

    return user
