"""Модуль конфигурации модели для осуществления запросов к внешнему сервису"""
from pydantic import BaseModel

from ..config.settings import CONTROLLER


class RequestModelResult(BaseModel):
    """Класс с данными для осуществления запроса к внешнему сервису"""
    method: str
    url: str
    data: dict | None = None


class RequestModel:
    """Класс для формирования модели для осуществления запросов к внешнему сервису"""

    def __init__(self, driver: str, method: str,
                 data: dict | None = None, url: str | None = None) -> None:
        data = data or {}
        self.url: str = CONTROLLER.url if not url else url
        self.driver: str = driver.lstrip('/')
        self.method: str = method.upper()
        self.data: dict = data

    def to_dict(self) -> dict:
        """Возвращает данные модели в виде словаря"""
        return {
            "url": self.url,
            "driver": self.driver,
            "method": self.method,
            "data": self.data,
        }

    def get_request(self) -> RequestModelResult:
        """Возвращает данные модели сформированные в запрос"""
        url = ""
        data = None
        if self.method == "GET":
            kwargs = ""
            for key, value in self.data.items():
                kwargs += f"{key}={value}&"
            url = f"{self.url}/{self.driver}?{kwargs}".lstrip('&')
        elif self.method == "POST":
            url = f'{self.url}/{self.driver}'
            data = self.data

        return RequestModelResult(method=self.method, url=url, data=data)
