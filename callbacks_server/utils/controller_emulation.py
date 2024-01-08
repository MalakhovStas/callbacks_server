"""Эмулятор контроллера для локального тестирования"""
from fastapi import FastAPI

app = FastAPI()

"""
Запуск эмулятора контроллера:
cd callbacks_server/utils/
uvicorn controller_emulation:app --port 8888 --reload

Туннель ngrok:
ngrok http 8888
"""


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {"status": 200, "message": "Emulation kontroller callbacks"}


@app.get("/callbacks/black_rabbit")
async def get_black_rabbit():
    """Callback endpoint GET BlackRabbit"""
    return {"status": 200, "message": "callback from black_rabbit driver received by controller"}


@app.post("/callbacks/black_rabbit")
async def post_black_rabbit():
    """Callback endpoint POST BlackRabbit"""
    return {"status": 200, "message": "callback from black_rabbit driver received by controller"}


@app.get("/callbacks/guava")
async def get_guava():
    """Callback endpoint GET Guava"""
    return {"status": 200, "message": "callback from guava driver received by controller"}


@app.post("/callbacks/guava")
async def post_guava():
    """Callback endpoint POST Guava"""
    return {"status": 200, "message": "callback from guava driver received by controller"}
