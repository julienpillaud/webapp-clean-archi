from cleanstack.fastapi.exceptions import ExceptionRegistry, add_exception_handler
from fastapi import FastAPI, status

from app.api.dev.router import router as dev_router
from app.api.dummies.router import router as dummies_router
from app.api.items.router import router as items_router
from app.api.logger import logger
from app.api.posts.router import router as posts_router
from app.api.users.router import router as users_router
from app.core.config import Settings
from app.domain.exceptions import CustomError


def create_fastapi_app(settings: Settings) -> FastAPI:
    logger.debug("Creating FastAPI app")
    app = FastAPI(
        title=settings.project_name,
        version=settings.api_version,
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )

    ExceptionRegistry.register(CustomError, status.HTTP_418_IM_A_TEAPOT)
    add_exception_handler(app=app)

    app.include_router(dev_router)
    app.include_router(dummies_router)
    app.include_router(items_router)
    app.include_router(posts_router)
    app.include_router(users_router)

    return app
