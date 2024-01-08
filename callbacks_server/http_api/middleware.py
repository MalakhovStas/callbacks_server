"""Модуль промежуточного ПО для обработки запросов к API"""
from asyncio.exceptions import TimeoutError  # pylint: disable=redefined-builtin
from json.decoder import JSONDecodeError

from async_timeout import timeout
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import ClientDisconnect
from starlette.responses import Response

from ..config.settings import (
    HTTP_API_DEFAULT_RESPONSES,
    HTTP_API_REQUESTS_TIMEOUT,
)


class MiddlewareAPI(BaseHTTPMiddleware):
    """Промежуточное ПО для валидации доступа к API"""

    def __init__(self, app):
        super().__init__(app)

    @staticmethod
    async def log_request(request) -> str:
        """Логирование входящего запроса"""
        client: str | None = (f'{request.client.host}:{request.client.port}'
                              if request.client else None)
        method: str = request.method
        url: str = request.url.components.path
        logger.debug(f'API-Request: {f"{client=} | " if client else ""}{method=} | {url=}')
        return url

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Основной метод промежуточной обработки входящих запросов"""
        await self.log_request(request)
        response = await self.try_call_next(request, call_next)
        return response

    @staticmethod
    async def try_call_next(request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Метод для обработки исключений не обработанных на уровне endpoints и
        формирования ответов пользователю на основании типа исключения"""
        try:
            # Контролирует время выполнения обработки запроса при превышении сбрасывает по Timeout
            async with timeout(HTTP_API_REQUESTS_TIMEOUT):
                response = await call_next(request)
        except ClientDisconnect:
            response = HTTP_API_DEFAULT_RESPONSES.client_disconnected()
        except TimeoutError:
            response = HTTP_API_DEFAULT_RESPONSES.timeout_error()
        except JSONDecodeError:
            response = HTTP_API_DEFAULT_RESPONSES.error_body_type()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.exception(exc)
            response = HTTP_API_DEFAULT_RESPONSES.unexpected_error()
        return response
