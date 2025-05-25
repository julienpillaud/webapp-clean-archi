import uuid

from pydantic import BaseModel

from app.domain.posts.entities import PostCreate, PostUpdate, TagName


class PostDTO(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    author_id: uuid.UUID
    tags: list[TagName]


class PostCreateDTO(PostCreate):
    def to_domain(self) -> PostCreate:
        return PostCreate.model_validate(self)


class PostUpdateDTO(PostUpdate):
    def to_domain(self) -> PostUpdate:
        return PostUpdate.model_validate(self)
