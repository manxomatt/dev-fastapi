from fastapi import FastAPI

from app.routers import items, users, auth
from app.core.logging_config import setup_logging
from app.middleware.request_logger import RequestLoggerMiddleware


def create_app() -> FastAPI:
    # configure logging early
    setup_logging()

    app = FastAPI(title="Dev FastAPI", version="0.1.0")

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"message": "Hello, World!"}

    # register middleware
    app.add_middleware(RequestLoggerMiddleware)

    app.include_router(items.router)
    app.include_router(users.router)
    app.include_router(auth.router)
    return app


app = create_app()