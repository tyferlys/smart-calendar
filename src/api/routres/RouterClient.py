import asyncio
from typing import List

from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.client import ClientCreateRequest, ClientCreateResponse, ClientGetResponse
from src.database.operations.operationsClient import create_client_database, get_client_database, get_clients_database, \
    update_client_database

routerClient = APIRouter()


@routerClient.get("", tags=["clients.get"])
async def get_clients(response: Response) -> List[ClientGetResponse]:
    try:
        clients = await get_clients_database()

        response.status_code = status.HTTP_200_OK
        return clients
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return []


@routerClient.get("/{phone}", tags=["clients.get"])
async def get_client(phone: str, response: Response) -> ClientGetResponse | None:
    try:
        client = await get_client_database(phone)

        if client is not None:
            response.status_code = status.HTTP_200_OK
            return client
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return


@routerClient.post("", tags=["clients.post"])
async def create_client(client: ClientCreateRequest, response: Response) -> ClientCreateResponse:
    try:
        await create_client_database(client)
        response.status_code = status.HTTP_201_CREATED
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return client


@routerClient.put("", tags=["clients.put"])
async def update_client(client: ClientCreateRequest, response: Response) -> ClientCreateResponse:
    try:
        await update_client_database(client)
        response.status_code = status.HTTP_200_OK
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return client
