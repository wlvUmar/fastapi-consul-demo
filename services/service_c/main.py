from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .infrastructure import registration
from .infrastructure.logging import setup_logging
from .routes import router

setup_logging(settings.service_id)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await registration.register()
    yield
    await registration.deregister()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.service_name, lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
