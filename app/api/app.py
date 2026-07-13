from fastapi import FastAPI

from app.api.exceptions import add_exception_handlers
from app.api.items.router import router as items_router
from app.api.lifespan import lifespan_factory
from app.api.posts.router import router as posts_router
from app.api.users.router import router as users_router
from app.core.config import Settings


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
        lifespan=lifespan_factory(settings=settings),
    )

    add_exception_handlers(app=app)

    app.include_router(posts_router)
    app.include_router(users_router)
    app.include_router(items_router)

    return app
