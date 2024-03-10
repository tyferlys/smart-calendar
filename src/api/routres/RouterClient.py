import asyncio
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.client import ClientCreateRequest, ClientCreateResponse, ClientGetResponse, \
    ClientUpdateRequest, ClientUpdateResponse, ClientGetAllResponse
from src.database.operations.operationsClient import create_client_database, get_client_database, get_clients_database, \
    update_client_database

routerClient = APIRouter()


@routerClient.get("", tags=["clients.get"])
async def get_clients(page: int, count: int, response: Response) -> ClientGetAllResponse | None:
    try:
        offset = (page - 1) * count
        limit = count
        clients = await get_clients_database(offset, limit)

        response.status_code = status.HTTP_200_OK
        return clients
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.get("/{phoneOrUsername}", tags=["clients.get"])
async def get_client(phoneOrUsername: str, response: Response) -> ClientGetResponse | None:
    try:
        client = await get_client_database(phoneOrUsername)

        if client is not None:
            response.status_code = status.HTTP_200_OK
            return client
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.post("", tags=["clients.post"])
async def create_client(client: ClientCreateRequest, response: Response) -> ClientCreateResponse | None:
    try:
        newClient = await create_client_database(client)
        response.status_code = status.HTTP_201_CREATED
        return newClient
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.put("", tags=["clients.put"])
async def update_client(client: ClientUpdateRequest, response: Response) -> ClientUpdateResponse | None:
    try:
        newClient = await update_client_database(client)
        response.status_code = status.HTTP_200_OK
        return newClient
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


