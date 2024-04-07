import datetime
from typing import List

from pydantic import BaseModel


class RecordCreateRequest(BaseModel):
    date_day: datetime.date
    id_service: int
    telegram_id: str
    time: datetime.time


class RecordCreateResponse(BaseModel):
    id: int
    id_day: int
    id_service: int
    id_client: int
    status: str
    time: datetime.time


class RecordGetRequest(BaseModel):
    date_day: datetime.date
    title_service: str
    time: datetime.time

