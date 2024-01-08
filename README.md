# Callbacks server



## Описание
Данный проект для системы CascadePoolController

## Локальное тестирование
Предусмотрен HTTP API для тестирования, для запуска 
необходимо:
1. Клонировать репозиторий на локальную машину или удалённый сервер командой:
   * <span style="color:green">git clone <адрес репозитория в сети></span>
2. Добавить в каталог env, файл <span style="color:green">.env.local</span> c секретными 
данными для доступа к внешнему сервису.
3. Выполнить команды для активации виртуального окружения Poetry 
(Poetry предварительно должен быть установлен в системе):
    * <span style="color:green">poetry config virtualenvs.in-project true</span>
    * <span style="color:green">poetry install</span>
    * <span style="color:green">poetry shell</span>
4. Выполнить команду для локального запуска проекта, также автоматически будет запущен HTTP API 
для тестирования:
    * <span style="color:green">python main.py</span>


* в ответе всегда возвращаются поля:<br>
    * <span style="color:green">**message**</span> - текстовое сообщение от внешнего сервиса или драйвера<br> 
    * <span style="color:green">**status**</span> - статус ответа, числовой код соответствует статусам протокола HTTP<br>
    * <span style="color:green">**error**</span> - логическое значение указывающее на наличие ошибки при обработке запроса<br>
