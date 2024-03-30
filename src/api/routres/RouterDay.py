import datetime
from typing import List

from fastapi import APIRouter, Response, status
from loguru import logger
from src.database.operations.operationDay import get_days_database

routerDay = APIRouter()


@routerDay.get("", tags=["days.get"])
async def get_days(beginDate: datetime.date, endDate: datetime.date, response: Response) -> List[int]:
    logger.info(f"Запрос на получение дней с данными: beginDate - {beginDate}, endDate - {endDate}")
    try:
        days = await get_days_database(beginDate, endDate)
        logger.info(f"Полученные дни - {days}")

        response.status_code = status.HTTP_200_OK
        return days
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


