import datetime
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import Settings
from app.domain.entities import Token

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(settings: Settings, subject: Any) -> Token:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=settings.access_token_expire_minutes,
    )
    encoded_jwt = jwt.encode(
        payload={"exp": expire, "sub": str(subject)},
        key=settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return Token(access_token=encoded_jwt, token_type="bearer")
