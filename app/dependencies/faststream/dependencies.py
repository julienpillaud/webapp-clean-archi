from typing import Annotated

from fast_depends import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.context import Context
from app.dependencies.fastapi.dependencies import get_session
from app.dependencies.settings import get_settings


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[Session, Depends(get_session)],
) -> Context:
    return Context(settings=settings, session=session)
