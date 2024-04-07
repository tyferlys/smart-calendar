import datetime
from typing import List

from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.record import RecordCreateRequest, RecordCreateResponse, RecordGetRequest
from loguru import logger

from src.database.operations.operationEvent import create_record_database, get_records_client_database

routerRecord = APIRouter()


# @routerRecord.get("", tags=["records.get"])
# async def get_records():
#     pass
#
#
@routerRecord.get("/{phoneOrTelegramId}", tags=["records.get"])
async def get_records_client(phoneOrTelegramId: str, response: Response) -> List[RecordGetRequest] | None:
    logger.info(f"Запрос на получение записией клиента: данные - {phoneOrTelegramId}")
    try:
        records = await get_records_client_database(phoneOrTelegramId)
        logger.info(f"Записи найдены - {len(records)}")

        response.status_code = status.HTTP_200_OK
        return records
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerRecord.post("", tags=["records.post"])
async def create_record(event: RecordCreateRequest, response: Response) -> RecordCreateResponse | None:
    logger.info(f"Запрос на создание записи: данные - {event}")
    try:
        newEvent = await create_record_database(event)
        logger.info(f"Запись создана: даные - {newEvent}")

        response.status_code = status.HTTP_201_CREATED
        return newEvent
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


# @routerRecord.put("", tags=["records.put"])
# async def update_record():
#     pass
