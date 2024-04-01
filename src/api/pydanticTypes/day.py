import datetime
from typing import List

from pydantic import BaseModel


class DayGetResponse(BaseModel):
    begin_time_free: datetime.time
    end_time_free: datetime.time
