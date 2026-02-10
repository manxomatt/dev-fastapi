from fastapi import FastAPI

from app.routers import items, users, auth


def create_app() -> FastAPI:
    app = FastAPI(title="Dev FastAPI", version="0.1.0")

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"message": "Hello, World!"}

    app.include_router(items.router)
    app.include_router(users.router)
    app.include_router(auth.router)
    return app


app = create_app()