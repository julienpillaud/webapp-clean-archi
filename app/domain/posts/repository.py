from typing import Protocol

from app.domain.interfaces.repository import BaseRepositoryProtocol
from app.domain.posts.entities import Post


class PostRepositoryProtocol(BaseRepositoryProtocol[Post], Protocol): ...
