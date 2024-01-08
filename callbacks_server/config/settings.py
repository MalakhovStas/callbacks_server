"""Модуль с основными настройками приложения"""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pytoml import parser  # type: ignore

from ..http_api.default_responses import DefaultResponses
from ..models.controller import Controller
from ..tools.requests_manager import RequestsManager

TIME_ZONE = 'Europe/Moscow'

if sys.argv[0].endswith('gunicorn'):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DEBUG = False
else:
    BASE_DIR = Path(sys.path[0])
    DEBUG = True

load_dotenv(dotenv_path=BASE_DIR.joinpath('env/.env.default'), override=True)
load_dotenv(dotenv_path=BASE_DIR.joinpath('env/.env.local'), override=True)

NETWORK: str = os.getenv('NETWORK', default='local')

CONTROLLER_CREDENTIALS: dict = json.loads(os.getenv("CONTROLLER_CREDENTIALS", default='{}'))

# Словарь с данными проекта из pyproject.toml
with open('pyproject.toml', 'r', encoding="utf-8") as file:
    PYPROJECT = parser.load(file)

# Настройки логирования
# при достижении *.log файла указанного размера -> файл сжимается в *.log.zip
LOGS_ROTATION = "10 mb"
# количество сжатых файлов для хранения, не более
LOGS_RETENTION = 1

# Настройки конфигурации HTTP API
HTTP_API_HOST = '0.0.0.0'
HTTP_API_PORT = 8000
PATH_TO_APP = "callbacks_server.http_api.base:app"
# Прерывание обработки входящего запроса в случае превышения указанного времени обработки секунд
HTTP_API_REQUESTS_TIMEOUT = 60
# Имя заголовка для передачи токена пользователя
# url доступа к callbacks
CALLBACKS_URL = "/callbacks"
# url доступа к техническим службам и инструментам сервера
TECHNICAL_URL = "/technical"
# Класс с набором стандартных ответов пользователю в зависимости от сложившейся ситуации
HTTP_API_DEFAULT_RESPONSES = DefaultResponses()

# Инициализация RequestManager для осуществления внешних запросов
REQUESTS_MANAGER = RequestsManager(
    default_content_type="application/json",
    max_requests_retries=1,  # кол-во повторных запросов при ошибке запроса
    requests_timeout=10,  # сброс запроса по исключению timeout, через - секунд
    use_proxy=False,  # если True запросы осуществляются только через прокси
    proxy=json.loads(os.getenv("PROXY", default='{}'))
)
# Инициализация модели данных контроллера
CONTROLLER = Controller(**{"name": "LightController", "url": "https://light_controller.com"})
