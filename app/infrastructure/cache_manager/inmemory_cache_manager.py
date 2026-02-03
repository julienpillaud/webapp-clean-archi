import builtins

from app.infrastructure.cache_manager.redis_cache_manager import RedisCacheManager

WRONG_TYPE_ERROR = "WRONGTYPE Operation against a key holding the wrong kind of value"


class RedisEmulator:
    def __init__(self) -> None:
        self.data: dict[str, str | set[str]] = {}

    def get(self, name: str) -> str | None:
        existing_value = self.data.get(name)
        if isinstance(existing_value, set):
            raise ValueError(WRONG_TYPE_ERROR)

        return existing_value

    def set(self, name: str, value: str, ex: int | None = None) -> None:
        self.data[name] = value

    def sadd(self, name: str, *values: str) -> None:
        existing_values = self.data.get(name, set())
        if isinstance(existing_values, str):
            raise ValueError(WRONG_TYPE_ERROR)

        self.data[name] = existing_values.union(set(values))

    def smembers(self, name: str) -> builtins.set[str]:
        existing_values = self.data.get(name, set())
        if isinstance(existing_values, str):
            raise ValueError(WRONG_TYPE_ERROR)

        return set(existing_values)

    def delete(self, *names: str) -> None:
        for name in names:
            self.data.pop(name, None)


class InMemoryCacheManager(RedisCacheManager):
    def __init__(self) -> None:
        super().__init__(RedisEmulator())  # type: ignore
