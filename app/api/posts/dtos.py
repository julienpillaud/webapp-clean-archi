from pydantic import BaseModel

from app.domain.entities import EntityId
from app.domain.posts.entities import PostCreate, PostUpdate, TagName


class PostDTO(BaseModel):
    id: EntityId
    title: str
    content: str
    author_id: EntityId
    tags: list[TagName]


class PostCreateDTO(PostCreate):
    def to_domain(self) -> PostCreate:
        return PostCreate.model_validate(self)


class PostUpdateDTO(PostUpdate):
    def to_domain(self) -> PostUpdate:
        return PostUpdate.model_validate(self)
