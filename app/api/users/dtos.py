from pydantic import BaseModel

from app.api.posts.dtos import PostDTO
from app.domain.entities import EntityId
from app.domain.users.entities import UserCreate, UserUpdate


class UserDTO(BaseModel):
    id: EntityId
    username: str
    email: str
    posts: list[PostDTO]


class UserCreateDTO(UserCreate):
    def to_domain(self) -> UserCreate:
        return UserCreate.model_validate(self)


class UserUpdateDTO(UserUpdate):
    def to_domain(self) -> UserUpdate:
        return UserUpdate.model_validate(self)
