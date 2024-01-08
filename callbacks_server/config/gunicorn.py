"""Модуль конфигурации Gunicorn"""
# pylint: disable=invalid-name
bind = "127.0.0.1:8000"

# Worker Options
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/malahov/callbacks_server/logs/access_log'
errorlog = '/home/malahov/callbacks_server/logs/error_log'
