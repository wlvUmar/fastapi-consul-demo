from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .infrastructure.http_client import close_client, init_client
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_client(settings.request_timeout)
    yield
    await close_client()


def create_app() -> FastAPI:
    app = FastAPI(title="API Gateway", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
