import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.routres.RouterClient import routerClient
from src.api.routres.RouterReport import routerReport
from src.api.routres.RouterService import routerService
from src.api.routres.RouterOwner import routerOwner


load_dotenv()
sourceToken = os.getenv("TOKEN")

app = FastAPI(title="Smart Calendar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routerClient, prefix="/clients", tags=["clients"])
app.include_router(routerOwner, prefix="/owner", tags=["owner"])
app.include_router(routerService, prefix="/services", tags=["services"])
app.include_router(routerReport, prefix="/reports", tags=["reports"])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    paths = [
        "/docs",
        "/openapi"
    ]

    if any(request.url.path.startswith(path) for path in paths):
        response = await call_next(request)
        return response
    else:
        try:
            token = request.headers["x-token"]

            if token == sourceToken:
                response = await call_next(request)
                return response
            else:
                response = JSONResponse(status_code=409, content={"message": "Invalid token"})
                return response
        except:
            response = JSONResponse(status_code=409, content={"message": "Invalid token"})
            return response


@app.get("/")
def read_root() -> str:
    return "Сервер работает"

