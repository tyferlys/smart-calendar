from pydantic import BaseModel


class ReportCreateRequest(BaseModel):
    telegram_id: str
    text: str


class ReportCreateResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    username: str
    telegram_id: str
    text: str