from cleanstack.entities import EntityId
from pydantic import BaseModel

from app.api.posts.dtos import PostDTO


class UserDTO(BaseModel):
    id: EntityId
    username: str
    email: str
    posts: list[PostDTO]
