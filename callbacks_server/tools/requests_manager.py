"""Модуль инструментов для отправки внешних запросов"""
from typing import Optional, Union, Dict, List, Any

import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType  # type: ignore
from loguru import logger

from ..base import BaseTools
from ..utils.misc import hide_secrets


class RequestsManager(BaseTools):
    """Единая точка для отправки внешних запросов"""

    def __init__(
            self,
            default_content_type: str,
            max_requests_retries: int,
            requests_timeout: int,
            use_proxy: bool,
            proxy: dict
    ):
        self.default_content_type = {"Content-Type": default_content_type}
        self.max_requests_retries = max_requests_retries
        self.requests_timeout = requests_timeout
        self.use_proxy = use_proxy
        self.proxy = proxy

    async def __call__(
            self,
            url: str,
            method: str = "get",
            headers: Optional[Dict] = None,
            data: Optional[Dict[Any, Any]] = None,
            step: int = 1,
    ) -> Union[Dict, List, None]:
        """Повторяет запрос/запросы, если нет ответа или исключение"""
        # если нет прокси - выход и логирование ошибки
        if self.use_proxy and not self.proxy:
            logger.error(f'{self.sign} no proxy!!!')
            return None

        # создаёт словарь заголовков
        if headers:
            headers = {**self.default_content_type, **headers}
        else:
            headers = self.default_content_type

        # вызывает основной метод отправки запроса
        result = await self.aio_request(
            url=url,
            headers=headers,
            method=method,
            data=data,
        )
        # результат пустой или None или не словарь повторяет запрос,
        # если шаг запроса меньше чем значение self.max_requests_retries
        if not result or not isinstance(result, dict):
            step += 1
            if step < self.max_requests_retries:
                result = await self.__call__(
                    url=url,
                    headers=headers,
                    method=method,
                    data=data,
                    step=step,
                )
        return result

    def __proxy_connector(self) -> ProxyConnector:
        """Возвращает прокси коннектор соединения"""
        proxy_types = {
            "http": ProxyType.HTTP,
            "https": ProxyType.HTTPS,
            "socks5": ProxyType.SOCKS5,
            "socks4": ProxyType.SOCKS4,
        }

        return ProxyConnector(
            proxy_type=proxy_types[self.proxy.get('type', '')],
            host=self.proxy.get('ip'),
            port=self.proxy.get('port'),
            username=self.proxy.get('login') if self.proxy.get('login') else None,
            password=self.proxy.get('password') if self.proxy.get('password') else None
        )

    async def aio_request(
            self,
            url: str,
            method: str = "get",
            headers: Optional[Dict] = None,
            data: Optional[Dict[Any, Any]] = None) -> Union[Dict, List]:
        """Основной метод http запросов, повторяет запрос,
        если во время выполнения запроса произошло исключение"""
        step = 1
        result: Dict[Any, Any] = {}
        # Если заголовки не переданы передаёт один заголовок
        # Content-Type со значением self.default_content_type
        if not headers:
            headers = self.default_content_type

        # Логирование входных данных для отправки запроса
        url_without_secrets, data_without_secrets = hide_secrets(url=url, data=data)
        logger.debug(f"{self.sign} {step=} -> request to: url={url_without_secrets} "
                     f"| {method=} | data={data_without_secrets} | {headers=}")

        if self.use_proxy:
            connector = self.__proxy_connector()
        else:
            connector = aiohttp.TCPConnector()

        async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
            # В случае исключения повторяет запрос,
            # если шаг запроса меньше чем значение self.max_requests_retries
            while step < self.max_requests_retries + 1:
                try:
                    if method.upper() == "POST":
                        # POST запрос
                        async with session.post(
                                url, json=data, timeout=self.requests_timeout) as response:
                            result = await self.__get_result(response=response)
                    else:
                        # GET запрос
                        async with session.get(url, timeout=self.requests_timeout) as response:
                            result = await self.__get_result(response=response, data=data)
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    # В случае исключения формирует словарь результата и логирует ошибку
                    result = {'response': {'error': f'{exc.__class__.__name__} {exc}'}, 'url': url}
                    result.update(data)
                    text = ("TRY AGAIN" if step < 3 else "BRAKE requests return ERROR")
                    logger.warning(f"{self.sign} ERROR -> {step=} -> {text} | {result=}")
                    step += 1
                else:
                    # Если успешно логирует ответ выходит из цикла и возвращает результат
                    logger.debug(f"{self.sign} SUCCEED -> {step=} | return={result}")
                    break
        return result

    async def __get_result(
            self,
            response: aiohttp.ClientResponse,
            data: Optional[Dict[Any, Any]] = None) -> Optional[Dict]:
        """Возвращает данные ответа"""
        result = None
        try:
            if response.content_type in ["text/html", "text/plain"]:
                # Формирует словарь ответа если тип контента строка
                result = {"response": await response.text()}
            else:
                # Формирует словарь ответа если тип контента json
                # для других ожидаемых типов контента нужно добавить обработку
                result = await response.json()

            if result and data:
                result.update(data)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            # В случае исключения логирует ошибку и возвращает None
            logger.error(f'{self.sign} {response.content_type=} | {exc=}')
        return result
