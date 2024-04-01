import datetime

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