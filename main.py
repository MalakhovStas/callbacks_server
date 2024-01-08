"""Основная точка входа для локального запуска HTTP интерфейса драйвера"""
from callbacks_server import interface


if __name__ == '__main__':
    interface.http()
