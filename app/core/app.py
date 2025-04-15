from fastapi import FastAPI

from app.api.dev.router import router as dev_router
from app.api.handlers import add_exceptions_handler
from app.api.posts.router import router as posts_router
from app.api.users.router import router as users_router

app = FastAPI(
    title="WebApp Clean Archi",
    swagger_ui_parameters={
        "tryItOutEnabled": True,
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
)
add_exceptions_handler(app=app)

app.include_router(dev_router)
app.include_router(posts_router)
app.include_router(users_router)
