from pydantic import BaseModel


class ReportCreateRequest(BaseModel):
    phone: str


class ReportCreateResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    username: str