import asyncio
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.client import ClientCreateRequest, ClientCreateResponse, ClientGetResponse, \
    ClientUpdateRequest, ClientUpdateResponse
from src.database.operations.operationsClient import create_client_database, get_client_database, get_clients_database, \
    update_client_database

routerClient = APIRouter()

load_dotenv()
token = os.getenv("TOKEN")


@routerClient.get("", tags=["clients.get"])
async def get_clients(tokenRequest: str, response: Response) -> List[ClientGetResponse]:
    try:
        if tokenRequest != token:
            response.status_code = status.HTTP_409_CONFLICT
            return []

        clients = await get_clients_database()

        response.status_code = status.HTTP_200_OK
        return clients
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return []


@routerClient.get("/{phone}", tags=["clients.get"])
async def get_client(tokenRequest: str, phone: str, response: Response) -> ClientGetResponse | None:
    try:
        if tokenRequest != token:
            response.status_code = status.HTTP_409_CONFLICT
            return None

        client = await get_client_database(phone)

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
async def create_client(tokenRequest: str, client: ClientCreateRequest, response: Response) -> ClientCreateResponse | None:
    try:
        if tokenRequest != token:
            response.status_code = status.HTTP_409_CONFLICT
            return None

        newClient = await create_client_database(client)
        response.status_code = status.HTTP_201_CREATED
        return newClient
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.put("", tags=["clients.put"])
async def update_client(tokenRequest: str, client: ClientUpdateRequest, response: Response) -> ClientUpdateResponse | None:
    try:
        if tokenRequest != token:
            response.status_code = status.HTTP_409_CONFLICT
            return None

        newClient = await update_client_database(client)
        response.status_code = status.HTTP_200_OK
        return newClient
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


