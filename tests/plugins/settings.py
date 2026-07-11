import pytest

from app.core.config import Settings
from tests.conftest import get_settings_override


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()
