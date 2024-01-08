"""Модуль конфигурации логирования"""

from typing import Any

from loguru import logger

from . import settings

LOGS_DIR = settings.BASE_DIR.joinpath('logs')

DEBUG_FORMAT = ("{time:DD-MM-YYYY at HH:mm:ss} | {level} | file: {file} "
                "| func: {function} | line: {line} | message: {message}")

ERRORS_FORMAT = "{time:DD-MM-YYYY at HH:mm:ss} | {level} | {file} | {message}"
SECURITY_FORMAT = "{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}"

logger_common_args: dict[str, Any] = {
    "diagnose": True,
    "backtrace": False,
    "rotation": settings.LOGS_ROTATION,
    "retention": settings.LOGS_RETENTION,
    "compression": "zip",
}

debug_log: dict[str, Any] = {
    "sink": LOGS_DIR.joinpath("debug.log"),
    "level": "DEBUG",
    "format": DEBUG_FORMAT,
    **logger_common_args
}
logger.add(**debug_log)

errors_log: dict[str, Any] = {
    "sink": LOGS_DIR.joinpath("errors.log"),
    "level": "WARNING",
    "format": ERRORS_FORMAT,
    **logger_common_args
}
logger.add(**errors_log)

request_manager_log: dict[str, Any] = {
    "sink": LOGS_DIR.joinpath("RequestsManager.log"),
    "level": "DEBUG",
    "format": DEBUG_FORMAT,
    "filter": lambda msg: msg.get("message").startswith('RequestsManager'),
    **logger_common_args
}
logger.add(**request_manager_log)
