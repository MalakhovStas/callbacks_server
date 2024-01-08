"""Модуль инициализации интерфейсов для взаимодействия с драйвером"""
import uvicorn

from .config import settings
from .server import Server

server = Server()


def http():
    """Запуск HTTP API"""
    uvicorn.run(
        settings.PATH_TO_APP,
        host=settings.HTTP_API_HOST,
        port=settings.HTTP_API_PORT,
        reload=True
    )
