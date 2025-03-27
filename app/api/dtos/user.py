import uuid

from pydantic import BaseModel

from app.domain.user.entities import UserCreate, UserUpdate


class UserDTO(BaseModel):
    id: uuid.UUID
    username: str
    email: str


class UserCreateDTO(UserCreate):
    def to_domain(self) -> UserCreate:
        return UserCreate.model_validate(self)


class UserUpdateDTO(UserUpdate):
    def to_domain(self) -> UserUpdate:
        return UserUpdate.model_validate(self)
