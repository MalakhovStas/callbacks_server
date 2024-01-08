"""Модуль базовой модели ответов интерфейса драйвера"""
from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Класс базовой модели ответов интерфейса драйвера"""
    message: str
    status: int
    error: bool


class ResponseConverter:  # pylint: disable=too-few-public-methods
    """Класс для преобразования ответа контроллера в ответ сервера внешнему сервису"""

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def driver_response(self) -> dict[str, Any]:
        """Метод формирования ответа от драйвера"""
        status = self.__dict__.get("status", None)
        message = self.__dict__.get("message", None)

        if status in [200, '200', 'ok', 'Ok', 'OK']:
            response = BaseResponse(
                message=message if message else "success",
                status=200,
                error=False,
            )

        else:
            response = BaseResponse(
                message=message if message else "failed",
                status=500,
                error=True
            )

        return response.model_dump()
