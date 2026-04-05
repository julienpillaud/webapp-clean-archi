from typing import Protocol

from cleanstack.domain import SyncRepositoryProtocol

from app.domain.posts.entities import Post


class PostRepositoryProtocol(SyncRepositoryProtocol[Post], Protocol): ...
