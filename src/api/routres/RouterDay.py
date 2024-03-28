import datetime
from typing import List

from fastapi import APIRouter, Response, status

from src.database.operations.operationDay import get_days_database

routerDay = APIRouter()


@routerDay.get("", tags=["days.get"])
async def get_days(beginDate: datetime.date, endDate: datetime.date, response: Response) -> List[int]:
    try:
        days = await get_days_database(beginDate, endDate)
        response.status_code = status.HTTP_200_OK
        return days
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


