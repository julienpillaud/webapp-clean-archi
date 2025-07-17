import inspect
from collections.abc import Callable
from typing import Annotated, Any, ClassVar, TypeVar, get_args, get_origin

T = TypeVar("T")


class Dependency:
    def __init__(self, dependency: Callable[..., Any]):
        self.dependency = dependency


def get_typed_annotation(annotation: Any) -> Any:
    if isinstance(annotation, str):
        raise ValueError("String annotations are not supported.")
    return annotation


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    signature = inspect.signature(call)
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param.annotation),
        )
        for param in signature.parameters.values()
    ]
    return inspect.Signature(typed_params)


def resolve_dependency(call: Callable[..., Any]) -> Any:
    signature = get_typed_signature(call)
    kwargs = {}

    for param_name, param in signature.parameters.items():
        # Case: param: Annotated[str, Dependency(func)]
        if get_origin(param.annotation) is Annotated:
            annotated_args = get_args(param.annotation)

            for metadata in annotated_args[1:]:
                if isinstance(metadata, Dependency):
                    dependency_func = metadata.dependency
                    kwargs[param_name] = resolve_dependency(dependency_func)
                    # Get the first dependency and break
                    break

        # Case: param = Depends(func)
        elif isinstance(param.default, Dependency):
            dependency_func = param.default.dependency
            kwargs[param_name] = resolve_dependency(dependency_func)

        elif param.default == inspect.Parameter.empty:
            raise ValueError("Cannot resolve dependency without default value.")

    return call(**kwargs)


class DependencyContainer:
    _overrides: ClassVar[dict[Callable[..., Any], Callable[..., Any]]] = {}

    @classmethod
    def resolve(cls, func: Callable[..., Any]) -> Any:
        if func in cls._overrides:
            override_func = cls._overrides[func]
            return resolve_dependency(override_func)
        else:
            return resolve_dependency(func)
