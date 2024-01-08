"""Модуль реализации драйверов сервера"""
from typing import Any


from .base import BaseServer
from .config.settings import REQUESTS_MANAGER
from .models.request import RequestModel, RequestModelResult
from .models.response import ResponseConverter


class Server(BaseServer):
    """Класс реализующий сервер"""

    def __init__(self):
        self.requests_manager = REQUESTS_MANAGER

    async def general_logic(self, request: RequestModelResult) -> dict[str, Any]:
        """Общая логика перенаправления входящих запросов к контроллеру"""
        # осуществляет запрос к внешнему сервису
        service_response = await self.requests_manager(
            method=request.method,
            url=request.url,
            data=request.data
        )
        # конвертирует результат ответа от внешнего сервиса в ответ от драйвера и возвращает его
        return ResponseConverter(**service_response).driver_response()

    async def black_rabbit(self, *args, **kwargs) -> dict[str, Any]:
        """Драйвер BlackRabbit"""
        request = RequestModel(
            driver='callbacks/black_rabbit',
            method='post',
            data=kwargs.get('data')
        ).get_request()
        return await self.general_logic(request=request)

    async def guava(self, *args, **kwargs) -> dict[str, Any]:
        """Драйвер Guava"""
        request = RequestModel(
            driver='callbacks/guava',
            method='post',
            data=kwargs.get('data')
        ).get_request()
        return await self.general_logic(request=request)
