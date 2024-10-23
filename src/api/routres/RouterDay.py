import datetime
from typing import List

from fastapi import APIRouter, Response, status
from loguru import logger

from src.api.pydanticTypes.day import DayGetResponse
from src.database.operations.operationDay import get_days_database, get_day_database

routerDay = APIRouter()


@routerDay.get("", tags=["days"])
async def get_days(beginDate: datetime.date, endDate: datetime.date, response: Response) -> List[int] | None:
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


@routerDay.get("/{dateDay}", tags=["days"])
async def get_day(dateDay: datetime.date, telegram_id: str, response: Response) -> DayGetResponse | None:
    logger.info(f"Запрос на получение информации о дне с данными: {datetime}")
    try:
        day = await get_day_database(dateDay, telegram_id)
        logger.info(f"Полученная информация - {day}")

        response.status_code = status.HTTP_200_OK
        return day
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None