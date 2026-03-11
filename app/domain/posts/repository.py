from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.posts.entities import Post


class PostRepositoryProtocol(RepositoryProtocol[Post], Protocol): ...
