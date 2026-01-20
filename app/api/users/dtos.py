from pydantic import BaseModel

from app.api.posts.dtos import PostDTO
from app.domain.entities import EntityId


class UserDTO(BaseModel):
    id: EntityId
    username: str
    email: str
    posts: list[PostDTO]
