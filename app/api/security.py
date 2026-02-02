import datetime
import logging

import jwt
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr, ValidationError

from app.core.config import Settings

logger = logging.getLogger(__name__)

# Utility class to get the bearer token from the Authorization header
# Allows direct JWT input in OpenAPI docs for easier testing.
http_bearer = HTTPBearer()


class JWTPayload(BaseModel):
    sub: str
    iat: datetime.datetime
    exp: datetime.datetime
    email: str | None = None


def decode_jwt(value: str | None, /, settings: Settings) -> JWTPayload | None:
    if not value:
        return None

    try:
        payload = jwt.decode(
            value,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
        )
    except jwt.PyJWTError as error:
        logger.warning("Invalid JWT token: %s", error)
        return None

    try:
        return JWTPayload(**payload)
    except ValidationError:
        return None


def encode_jwt(
    sub: str,
    email: EmailStr | None = None,
    *,
    settings: Settings,
) -> str:
    current_time = datetime.datetime.now(datetime.UTC)
    payload = {
        "sub": sub,
        "aud": settings.jwt_audience,
        "iat": current_time,
        "exp": current_time + datetime.timedelta(hours=1),
    }
    if email:
        payload["email"] = email

    return jwt.encode(
        payload,
        key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
