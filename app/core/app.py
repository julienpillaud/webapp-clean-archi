from fastapi import FastAPI

from app.api.handlers import add_exception_handler
from app.api.posts.router import router as posts_router
from app.api.users.router import router as users_router

app = FastAPI()
add_exception_handler(app=app)

app.include_router(posts_router)
app.include_router(users_router)
