import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from configProject import get_settings
from src.api.routres.RouterClient import routerClient
from src.api.routres.RouterDay import routerDay
from src.api.routres.RouterOptionClient import routerOptionClient
from src.api.routres.RouterRecord import routerRecord
from src.api.routres.RouterReport import routerReport
from src.api.routres.RouterService import routerService
from src.api.routres.RouterOwner import routerOwner
from src.database.configDataBase import create_tables
from src.database.models.models import create_admin

settings = get_settings()
app = FastAPI(title="Smart Calendar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await create_tables()
    await create_admin()

app.include_router(routerClient, prefix="/clients", tags=["clients"])
app.include_router(routerOwner, prefix="/owner", tags=["owner"])
app.include_router(routerService, prefix="/services", tags=["services"])
app.include_router(routerReport, prefix="/reports", tags=["reports"])
app.include_router(routerOptionClient, prefix="/options_clients", tags=["options_clients"])
app.include_router(routerRecord, prefix="/records", tags=["records"])
app.include_router(routerDay, prefix="/days", tags=["days"])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    paths = [
        "/docs",
        "/openapi",
        "/owner/login"
    ]
    if any(request.url.path.startswith(path) for path in paths) or settings.MODE == "dev":
        response = await call_next(request)
        return response
    else:
        if "x-token" not in request.headers:
            logger.info(f"Отправлен запрос: ip - {request.client.host} без x-token, на url {request.url}")
            response = JSONResponse(status_code=409, content={"message": "Invalid tokens"})
            return response

        token = request.headers["x-token"]

        if token == settings.TOKEN:
            response = await call_next(request)
            return response
        else:
            logger.info(f"Отправлен запрос: ip - {request.client.host} с неправильным x-token")
            response = JSONResponse(status_code=409, content={"message": "Invalid token"})
            return response


@app.get("/")
def read_root() -> str:
    return "Сервер работает"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API умного календаря",
        version="0.4.0",
        description="Лишний раз не бузи",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#TODO ЗАПИСЬ КЛИЕНТА, ПОЛУЧЕНИЕ ЗАПИСЕЙ ДЛЯ КЛИЕНТА
#TODO РОМА ДЕЛАЕТ НАСТРОЙКИ НОВЫЕ - НОВАЯ ЛОГИКА ВЫВОДА ЗАПИСЕЙ - НОВАЯ ЛОГИКА ЗАПИСИ