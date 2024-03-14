import asyncio
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.optionClient import OptionClientGetResponse, OptionClientUpdateRequest, \
    OptionClientUpdateResponse
from src.database.operations.operationOptionClient import get_option_client_database, update_option_client_database

routerOptionClient = APIRouter()


@routerOptionClient.get("/{phoneOrTelegramId}", tags=["options_clients.get"])
async def get_option_client(phoneOrTelegramId: str, response: Response) -> OptionClientGetResponse:
    try:
        option = await get_option_client_database(phoneOrTelegramId)
        response.status_code = status.HTTP_200_OK
        return option
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerOptionClient.put("", tags=["options_clients.put"])
async def get_option_client(optionClient: OptionClientUpdateRequest, response: Response) -> OptionClientUpdateResponse | None:
    try:
        newOption = await update_option_client_database(optionClient)
        response.status_code = status.HTTP_200_OK
        return newOption
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None
