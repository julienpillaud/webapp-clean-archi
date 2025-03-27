from pydantic import BaseModel

from app.domain.entities import DomainModel


class User(DomainModel):
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
