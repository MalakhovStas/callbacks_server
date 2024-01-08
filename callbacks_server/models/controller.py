"""Модуль конфигурации модели для хранения данных сервиса"""
from typing import Any

from pydantic import BaseModel


class Controller(BaseModel):
    """Модель для удобства хранения и обращения к данным контроллера"""
    name: str
    url: str
    interface: Any | None = None
    hidden_fields: list = []  # список полей скрытых для логирования
