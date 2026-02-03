from typing import Any, Protocol


class CacheManagerProtocol(Protocol):
    def set(
        self,
        key: str,
        value: str,
        ttl: int,
        tag: str | None = None,
    ) -> None: ...

    def get(self, key: str) -> Any | None: ...

    def invalidate_tag(self, tag: str) -> None: ...
