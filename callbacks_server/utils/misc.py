"""Модуль дополнительных инструментов"""
from art import tprint  # type: ignore
from colorama import Fore

from ..config import settings


def print_logo() -> None:
    """Приветственная заставка в консоли"""
    if settings.DEBUG:
        print(Fore.LIGHTGREEN_EX)
        tprint(settings.CONTROLLER.name + " callbacks - server")
        print(Fore.RESET)


def hide_secrets(url: str, data: dict | None) -> tuple[str, dict | None]:
    """Сокрытие секретных данных для логирования"""
    hide_symbols = '#' * 5
    # заменяет значения секретов переданных в url на #
    url_list: list = url.split('?')
    url_without_secrets: str = url_list[0]
    if len(url_list) > 1:
        url_without_secrets += '?'
        for argument in url_list[1].split('&'):
            if argument and (arg_name := argument.split('=')[0]):
                if arg_name in settings.CONTROLLER.hidden_fields:
                    url_without_secrets += ('&' + arg_name + '=' + hide_symbols)
                else:
                    url_without_secrets += '&' + argument

    # заменяет значения секретов переданных в data на #
    data_without_secrets: dict | None = data
    if data:
        data_without_secrets = {
            key: value if key not in settings.CONTROLLER.hidden_fields
            else hide_symbols for key, value in data.items()}

    return url_without_secrets, data_without_secrets
