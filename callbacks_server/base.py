"""Модуль формирования абстрактных базовых инструментов драйвера"""
# pylint: disable=unused-argument, too-few-public-methods
from abc import ABC
from datetime import datetime
from types import FunctionType
from typing import Any

from loguru import logger

from .models.response import BaseResponse


class BaseTools(ABC):
    """Базовый класс инструментов сервера для применения
    паттерна 'Singleton' ко всем инструментам"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.sign = cls.__name__ + ":"
            cls.__instance = super().__new__(cls)
        return cls.__instance


class DefaultResponses(ABC):
    """Базовый класс стандартных ответов интерфейса драйвера"""

    driver_not_implemented = BaseResponse(
        message="Driver not implemented", status=501, error=True
    ).model_dump()

    unexpected_server_error = BaseResponse(
        message="Unexpected server error",
        status=500,
        error=True).model_dump()


class ServerInterface(DefaultResponses, ABC):
    """Базовый абстрактный класс интерфейса сервера"""
    sign = 'ServerInterface:'

    def __get_driver(self, driver: str) -> FunctionType:
        """Возвращает метод драйвера, если в драйвере существует метод с именем == operation,
        если метода с таким именем в драйвере нет возвращает - DriverInterface.default_response"""

        async def default_response(*args, **kwargs) -> dict:
            """Метод ответа в случае, если запрашиваемый метод отсутствует в драйвере"""
            return BaseResponse(
                message=f"The requested '{driver=}' is missing",
                status=404,
                error=True,
            ).model_dump()

        if hasattr(self, driver):
            server_driver = getattr(self, driver)
        else:
            server_driver = default_response
        return server_driver

    async def __call__(self, driver: str, data: dict | None = None) -> dict:
        """Основной метод обращения к серверу, принимает 2 аргумента:
           driver (str) - строковое представление имени драйвера
           data (dict) - словарь с данными (default {})"""
        data = data or {}

        logger.info(f'{self.sign} incoming request: {datetime.utcnow()} | {driver=} | {data=}')

        try:
            server_driver = self.__get_driver(driver=driver)
            response = await server_driver(data=data)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.exception(exc)
            response = self.unexpected_server_error

        logger.info(f'{self.sign} | {datetime.utcnow()} | {response=}')
        return response


class BaseServer(ServerInterface, DefaultResponses, ABC):
    """Базовый абстрактный класс сервера, для предварительного объявления
    драйверов"""

    async def black_rabbit(self, *args, **kwargs) -> dict[str, Any]:
        """Драйвер BlackRabbit"""
        return self.driver_not_implemented

    async def guava(self, *args, **kwargs) -> dict[str, Any]:
        """Драйвер Guava"""
        return self.driver_not_implemented
