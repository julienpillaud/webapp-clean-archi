from pydantic import BaseModel, EmailStr

from app.domain.entities import DomainModel
from app.domain.posts.entities import Post


class User(DomainModel):
    email: EmailStr
    username: str
    hashed_password: str
    posts: list[Post]


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
