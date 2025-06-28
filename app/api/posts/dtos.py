from pydantic import BaseModel

from app.domain.entities import EntityId
from app.domain.posts.entities import TagName


class PostDTO(BaseModel):
    id: EntityId
    title: str
    content: str
    author_id: EntityId
    tags: list[TagName]
