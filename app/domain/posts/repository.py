from typing import Protocol

from app.domain.interfaces.repository import RepositoryProtocol
from app.domain.posts.entities import Post


class PostRepositoryProtocol(RepositoryProtocol[Post], Protocol): ...
