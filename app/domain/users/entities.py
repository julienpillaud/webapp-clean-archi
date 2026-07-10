from cleanstack import BaseEntity
from pydantic import EmailStr

from app.domain.posts.entities import Post


class User(BaseEntity):
    email: EmailStr
    username: str
    posts: list[Post]
