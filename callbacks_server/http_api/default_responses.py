"""Модуль формирования стандартных HTTP ответов пользователю от HTTP API интерфейса"""

from loguru import logger
from starlette.responses import JSONResponse


class DefaultResponses:
    """Класс для формирования стандартных HTTP ответов сервису"""

    @staticmethod
    def response(message: str, status: int, error: bool, **kwargs) -> JSONResponse:
        """Метод формирования JSON ответа на основе переданных данных"""
        response_content = {"message": message, "status": status, "error": error}
        response_content.update({**kwargs})
        logger.debug(f"API-Response: {response_content}")

        return JSONResponse(
            status_code=status,
            content=response_content
        )

    def forbidden(self) -> JSONResponse:
        """Доступ к API запрещён"""
        return self.response(message="Forbidden", status=403, error=True)

    def unauthorized(self) -> JSONResponse:
        """Пользователь не представился - в запросе отсутствует заголовок settings.TOKEN_HEADER"""
        return self.response(
            message="Unauthorized, expected token header", status=401, error=True)

    def driver_not_implemented(self) -> JSONResponse:
        """Запрашиваемый драйвер не реализован"""
        return self.response(message="Method not implemented", status=501, error=True)

    def error_body_type(self) -> JSONResponse:
        """Ошибка типа данных переданных пользователем в теле запроса"""
        return self.response(
            message="Type error, request body, expected json", status=415, error=True)

    def unexpected_error(self) -> JSONResponse:
        """Непредвиденная ошибка на стороне API"""
        return self.response(
            message="Unexpected error", status=500, error=True)

    def timeout_error(self) -> JSONResponse:
        """Ошибка времени обработки запроса на стороне API"""
        return self.response(
            message="Request Timeout", status=408, error=True)

    def client_disconnected(self) -> JSONResponse:
        """Клиент закрыл соединение, пока API обрабатывал запрос"""
        return self.response(
            message="Client Closed Request", status=499, error=True)
