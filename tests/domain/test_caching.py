from pydantic import BaseModel

from app.domain.caching import build_cache_key
from app.domain.context import ContextProtocol


class ReturnType(BaseModel):
    x: str


def command(context: ContextProtocol, /, a: int, b: str) -> ReturnType:
    return ReturnType(x="hello")


def test_build_cache_key_same_args() -> None:
    key1 = build_cache_key(command, 1, "hello")
    key2 = build_cache_key(command, 1, "hello")

    assert key1 == key2


def test_build_cache_key_different_args() -> None:
    key1 = build_cache_key(command, 1, "hello")
    key2 = build_cache_key(command, 2, "hello")

    assert key1 != key2


def test_build_cache_key_kwargs_order_doesnt_matter() -> None:
    key1 = build_cache_key(command, a=1, b="hello")
    key2 = build_cache_key(command, b="hello", a=1)

    assert key1 == key2
