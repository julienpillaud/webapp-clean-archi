from typing import cast

from app.core.config import Settings
from app.domain.interfaces.cache_manager import CacheManagerProtocol
from app.infrastructure.cache_manager.provider import RedisProvider


class RedisCacheManager(CacheManagerProtocol):
    def __init__(self, settings: Settings):
        RedisProvider.init(settings)
        self.client = RedisProvider.get_client()

    def set(
        self,
        key: str,
        value: str,
        ttl: int,
        tag: str | None = None,
    ) -> None:
        self.client.set(name=key, value=value, ex=ttl)

        if tag:
            tag_key = f"tag:{tag}"
            self.client.sadd(tag_key, key)

    def get(self, key: str) -> str | None:
        return cast(str | None, self.client.get(name=key))

    def invalidate_tag(self, tag: str) -> None:
        tag_key = f"tag:{tag}"
        keys_to_delete = self.client.smembers(tag_key)
        if not keys_to_delete:
            return

        self.client.delete(*keys_to_delete, tag_key)  # type: ignore[misc]
