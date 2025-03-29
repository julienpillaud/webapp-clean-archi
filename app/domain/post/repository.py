from typing import Protocol

from app.domain.interfaces.repository import BaseRepositoryProtocol
from app.domain.post.entities import Post


class PostRepositoryProtocol(BaseRepositoryProtocol[Post], Protocol): ...
