from typing import Annotated

import pytest

from app.core.dependencies import Dependency, resolve_dependency


def hello_world() -> str:
    return "hello_world"


def test_dependency_call_without_param() -> None:
    def call_without_param() -> str:
        return "call_without_param"

    result = resolve_dependency(call_without_param)
    assert result == "call_without_param"


def test_dependency_call_with_param() -> None:
    def call_without_default(param: str) -> str:
        return f"call_without_default: {param}"

    with pytest.raises(ValueError) as excinfo:
        resolve_dependency(call_without_default)
    assert str(excinfo.value) == "Cannot resolve dependency without default value."


def test_dependency_call_with_param_and_default() -> None:
    def call_with_default(param: str = "default") -> str:
        return f"call_with_default: {param}"

    result = resolve_dependency(call_with_default)
    assert result == "call_with_default: default"


def test_dependency_call_with_dependency() -> None:
    def call_with_dependency(param: str = Dependency(hello_world)) -> str:  # type: ignore
        return f"call_with_dependency: {param}"

    result = resolve_dependency(call_with_dependency)
    assert result == "call_with_dependency: hello_world"


def test_dependency_call_with_annotated_dependency() -> None:
    def call_with_annotated_dependency(
        param: Annotated[str, Dependency(hello_world)],
    ) -> str:
        return f"call_with_annotated_dependency: {param}"

    result = resolve_dependency(call_with_annotated_dependency)
    assert result == "call_with_annotated_dependency: hello_world"


def test_dependency_call_with_multiple_metadata() -> None:
    def call_with_annotated_dependency(
        param: Annotated[str, Dependency(hello_world), "metadata"],
    ) -> str:
        return f"call_with_annotated_dependency: {param}"

    result = resolve_dependency(call_with_annotated_dependency)
    assert result == "call_with_annotated_dependency: hello_world"


def test_dependency_nested_dependencies() -> None:
    def get_settings() -> str:
        return "settings"

    def get_context(settings: Annotated[str, Dependency(get_settings)]) -> str:
        return f"context_with_{settings}"

    def get_domain(context: Annotated[str, Dependency(get_context)]) -> str:
        return f"domain_with_{context}"

    result = resolve_dependency(get_domain)
    assert result == "domain_with_context_with_settings"


def test_dependency_multiple_dependencies() -> None:
    def get_settings() -> str:
        return "settings"

    def get_context() -> str:
        return "context"

    def get_domain(
        settings: Annotated[str, Dependency(get_settings)],
        context: Annotated[str, Dependency(get_context)],
    ) -> str:
        return f"domain_with_{context}_with_{settings}"

    result = resolve_dependency(get_domain)
    assert result == "domain_with_context_with_settings"
