from fastapi import FastAPI

from app.api.handlers import add_exception_handler
from app.api.routers.posts import router as posts_router
from app.api.routers.users import router as users_router

app = FastAPI()
add_exception_handler(app=app)

app.include_router(posts_router)
app.include_router(users_router)
