"""Модуль создания основной точки запуска FastAPI приложения"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from . import docs
from .endpoints.callbacks import callbacks_router
from .endpoints.technical import technical_router
from .middleware import MiddlewareAPI
from ..config import settings
from ..utils.misc import print_logo


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable = redefined-outer-name, unused-argument
    """Асинхронный менеджер контекста, выполняет код до запуска
    приложения FastAPI и после его завершения"""
    try:
        if settings.DEBUG:
            print_logo()
        yield
    except Exception as exc:  # pylint: disable = broad-exception-caught
        logger.exception(exc)


app = FastAPI(
    lifespan=lifespan,
    openapi_tags=docs.tags_metadata,
    title=docs.app_name,
    description=docs.app_description,
    version=docs.app_version
)
app.add_middleware(MiddlewareAPI)
app.include_router(
    technical_router, prefix=settings.TECHNICAL_URL, tags=[settings.TECHNICAL_URL.lstrip('/')])
app.include_router(
    callbacks_router, prefix=settings.CALLBACKS_URL, tags=[settings.CALLBACKS_URL.lstrip('/')])
