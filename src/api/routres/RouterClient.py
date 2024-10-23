import asyncio
import os
from typing import List
from loguru import logger
from dotenv import load_dotenv
from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.client import ClientCreateRequest, ClientCreateResponse, ClientGetResponse, \
    ClientUpdateRequest, ClientUpdateResponse, ClientGetAllResponse
from src.database.operations.operationsClient import create_client_database, get_client_database, get_clients_database, \
    update_client_database

routerClient = APIRouter()

@routerClient.get("", tags=["clients"])
async def get_clients(page: int, count: int, response: Response) -> ClientGetAllResponse | None:
    logger.info(f"Запрос на получение клиентов с данными: page - {page}, count - {count}")
    try:
        offset = (page - 1) * count
        limit = count
        clients = await get_clients_database(offset, limit)
        logger.info(f"Получено клиентов - {len(clients.clients)}")

        response.status_code = status.HTTP_200_OK
        return clients
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.get("/{phoneOrTelegramId}", tags=["clients"])
async def get_client(phoneOrTelegramId: str, response: Response) -> ClientGetResponse | None:
    logger.info(f"Запрос на получение клиента: данные - {phoneOrTelegramId}")
    try:
        client = await get_client_database(phoneOrTelegramId)
        logger.info(f"Получен клиент - {client}")

        if client is not None:
            response.status_code = status.HTTP_200_OK
            return client
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.post("", tags=["clients"])
async def create_client(client: ClientCreateRequest, response: Response) -> ClientCreateResponse | None:
    logger.info(f"Запрос на создания клиента: данные - {client}")
    try:
        newClient = await create_client_database(client)
        logger.info(f"Клиент создался - {newClient}")
        response.status_code = status.HTTP_201_CREATED
        return newClient
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerClient.put("", tags=["clients"])
async def update_client(client: ClientUpdateRequest, response: Response) -> ClientUpdateResponse | None:
    logger.info(f"Запрос на обновление клиента: данные - {client}")
    try:
        newClient = await update_client_database(client)
        logger.info(f"Клиент обновился - {newClient}")
        response.status_code = status.HTTP_200_OK
        return newClient
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


