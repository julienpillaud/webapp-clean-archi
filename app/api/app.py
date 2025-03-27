from fastapi import FastAPI

from app.api.handlers import add_exception_handler
from app.api.routes.users import user_router_factory
from app.domain.domain import Domain


def app_factory(domain: Domain):
    app = FastAPI()

    app.include_router(user_router_factory(domain=domain))
    add_exception_handler(app=app)

    return app
