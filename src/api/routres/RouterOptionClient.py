import asyncio
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status
from loguru import logger

from src.api.pydanticTypes.optionClient import OptionClientGetResponse, OptionClientUpdateRequest, \
    OptionClientUpdateResponse
from src.database.operations.operationOptionClient import get_option_client_database, update_option_client_database

routerOptionClient = APIRouter()


@routerOptionClient.get("/{phoneOrTelegramId}", tags=["options_clients.get"])
async def get_option_client(phoneOrTelegramId: str, response: Response) -> OptionClientGetResponse | None:
    logger.info(f"Запрос на настроек пользователя: данные - {phoneOrTelegramId}")
    try:
        option = await get_option_client_database(phoneOrTelegramId)
        logger.info(f"Настройки получены: настройки - {option}")
        if option is not None:
            response.status_code = status.HTTP_200_OK
            return option
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerOptionClient.put("", tags=["options_clients.put"])
async def get_option_client(optionClient: OptionClientUpdateRequest,
                            response: Response) -> OptionClientUpdateResponse | None:
    logger.info(f"Запрос на обновление настроек пользователя: данные - {optionClient}")
    try:
        newOption = await update_option_client_database(optionClient)
        logger.info(f"Настройки обновились: данные - {newOption}")
        response.status_code = status.HTTP_200_OK
        return newOption
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None
