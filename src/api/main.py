from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routres.RouterClient import routerClient
from src.api.routres.RouterOwner import routerOwner

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


@app.get("/")
def read_root() -> str:
    return "Сервер работает!"
