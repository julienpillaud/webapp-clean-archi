from cleanstack.entities import DomainEntity
from pydantic import EmailStr

from app.domain.posts.entities import Post


class User(DomainEntity):
    provider_id: str
    email: EmailStr
    username: str
    posts: list[Post]
