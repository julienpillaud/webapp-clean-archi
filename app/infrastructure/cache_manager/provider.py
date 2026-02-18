from redis import Redis

from app.core.config import Settings
from app.infrastructure.cache_manager.logger import logger


class RedisProvider:
    _client: Redis | None = None

    @classmethod
    def init(cls, settings: Settings, /) -> None:
        if cls._client is None:
            logger.debug("Initializing Redis client")
            cls._client = Redis.from_url(
                str(settings.redis_dsn),
                decode_responses=True,
            )

    @classmethod
    def get_client(cls) -> Redis:
        if cls._client is None:
            raise RuntimeError("Not initialized.")
        return cls._client
