"""Модуль с url endpoints API для взаимодействия с внешним сервисом"""
from json import JSONDecodeError

from fastapi import Request, APIRouter
from starlette.responses import JSONResponse

from ... import interface
from ...config.settings import HTTP_API_DEFAULT_RESPONSES

callbacks_router = APIRouter()


@callbacks_router.get("/{driver}")
async def get(driver: str, request: Request) -> JSONResponse:
    """**Для обращения к HTTP API методом GET, путь - callbacks/{driver}. В зависимости от
    значения {driver}, запрос перенаправляется в одноимённый url контроллера, если он существует,
    иначе сервер возвращает стандартный ответ(driver is missing). Данные которые необходимо
    передать серверу прописываются в url по схеме
    http://{host}:{port}/callbacks/{driver}?param1=value&param2=value**"""
    result = await interface.server(
        driver=driver,
        data=dict(request.query_params)
    )
    return HTTP_API_DEFAULT_RESPONSES.response(**result)


@callbacks_router.post("/{driver}")
async def post(driver: str, request: Request) -> JSONResponse:
    """**Для обращения к HTTP API методом POST, путь - callbacks/{driver}. В зависимости от
    значения {driver},  запрос перенаправляется в одноимённый url контроллера, если он существует,
    иначе сервер возвращает стандартный ответ(driver is missing). Данные которые необходимо
    передать серверу передаются в теле запроса в виде JSON по url
    http://{host}:{port}/callbacks/{driver}**"""
    try:
        data = await request.json()
    except JSONDecodeError:
        data = None

    result = await interface.server(
        driver=driver,
        data=data
    )
    return HTTP_API_DEFAULT_RESPONSES.response(**result)
