from fast_depends import dependency_provider

from app.event_handler.dependencies import get_context, get_settings
from tests.dependencies.dependencies import get_context_override, get_settings_override


def apply_faststream_overrides() -> None:
    dependency_provider.override(get_settings, get_settings_override)
    dependency_provider.override(get_context, get_context_override)
