from pydantic import BaseModel

from app.domain.entities import DomainModel
from app.domain.post.entities import Post


class User(DomainModel):
    username: str
    email: str
    posts: list[Post]


class UserCreate(BaseModel):
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
