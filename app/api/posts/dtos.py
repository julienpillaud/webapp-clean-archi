from cleanstack.entities import EntityId
from pydantic import BaseModel

from app.domain.posts.entities import TagName


class PostDTO(BaseModel):
    id: EntityId
    title: str
    content: str
    author_id: EntityId
    tags: list[TagName]
