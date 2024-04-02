import datetime

from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.record import RecordCreateRequest, RecordCreateResponse
from loguru import logger

from src.database.operations.operationEvent import create_client_database

routerRecord = APIRouter()


# @routerRecord.get("", tags=["records.get"])
# async def get_records():
#     pass
#
#
# @routerRecord.get("/client", tags=["records.get"])
# async def get_records_client(phoneOrTelegramId: str):
#     pass


@routerRecord.post("", tags=["records.post"])
async def create_record(event: RecordCreateRequest, response: Response) -> RecordCreateResponse | None:
    logger.info(f"Запрос на создание записи: данные - {event}")
    try:
        newEvent = await create_client_database(event)
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
