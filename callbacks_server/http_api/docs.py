"""Модуль конфигурации документирования swagger"""
from ..config import settings

app_name = settings.PYPROJECT['tool']['poetry']['name'].title() + " 🚀"
app_description = f"# {settings.PYPROJECT['tool']['poetry']['description']}"  # можно MD
app_version = settings.PYPROJECT['tool']['poetry']['version']

CALLBACKS_DESCRIPTION = f'''
### Callbacks endpoints
Обращение к каждой из конечных точек возможно при помощи GET и POST запросов.<br>

* url для ***GET*** запроса -
**[http://[host]:[port]/callbacks/[driver]?param1=value&param2=value]()**
 
* url для ***POST*** запроса - **[http://[host]:[port]/callbacks/[driver]]()**
и данные в формате JSON в теле запроса

### Конечные точки сервера:
* **<span style="color:green">callbacks/black_rabbit</span>**
* **<span style="color:green">callbacks/guava</span>**
'''

TECHNICAL_DESCRIPTION = '''### Технические методы 🛠
* **<span style="color:green">ping</span>** - проверка связи
* **<span style="color:green">set_host_controller</span>** - установка хоста контроллера на 
который будут перенаправляться callbacks от сервисов драйверов. Конечные точки контроллера должны
соответствовать конечным точкам сервера: callbacks/black_rabbit и callbacks/guava
'''

tags_metadata = [
    {
        "name": settings.CALLBACKS_URL.lstrip('/'),
        "description": CALLBACKS_DESCRIPTION,
    },
    {
        "name": settings.TECHNICAL_URL.lstrip('/'),
        "description": TECHNICAL_DESCRIPTION
    },
]
