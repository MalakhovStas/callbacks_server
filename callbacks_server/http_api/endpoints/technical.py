"""Модуль с техническими url endpoints API"""
from json import JSONDecodeError

from fastapi import Request, APIRouter

from ...config.settings import PYPROJECT, HTTP_API_DEFAULT_RESPONSES, CONTROLLER

technical_router = APIRouter()


@technical_router.get("/ping")
async def get_ping(request: Request):  # pylint: disable=unused-argument
    """**Метод проверки соединения**"""
    return HTTP_API_DEFAULT_RESPONSES.response(
        message=f"{PYPROJECT['tool']['poetry']['description']}", status=200, error=False)


@technical_router.post("/ping")
async def post_ping(request: Request):  # pylint: disable=unused-argument
    """**Метод проверки соединения**"""
    return HTTP_API_DEFAULT_RESPONSES.response(
        message=f"{PYPROJECT['tool']['poetry']['description']}", status=200, error=False)


def logic_set_host_controller(data):
    """Общая логика конечных точек"""
    if controller_host := data.get("controller_host"):
        CONTROLLER.url = controller_host
        result = HTTP_API_DEFAULT_RESPONSES.response(
            message="Controller host changed", status=200, error=False)
    else:
        result = HTTP_API_DEFAULT_RESPONSES.response(
            message="To set the host, you must pass the "
                    "controller_host argument containing the host url",
            status=400, error=True)
    return result


@technical_router.get("/set_host_controller")
async def post_set_host_controller(request: Request):  # pylint: disable=unused-argument
    """**Метод установки хоста контроллера для передачи входящих callbacks**"""
    data = dict(request.query_params) or {}
    return logic_set_host_controller(data)


@technical_router.post("/set_host_controller")
async def post_set_host_controller(request: Request):  # pylint: disable=unused-argument
    """**Метод установки хоста контроллера для передачи входящих callbacks**"""
    try:
        data = await request.json()
    except JSONDecodeError:
        data = {}
    return logic_set_host_controller(data)



