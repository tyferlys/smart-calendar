from pydantic import BaseModel


class OptionClientGetResponse(BaseModel):
    id: int
    id_client: int
    is_notification: bool
    timezone: int


class OptionClientUpdateRequest(BaseModel):
    id: int
    id_client: int
    is_notification: bool
    timezone: int


class OptionClientUpdateResponse(OptionClientUpdateRequest):
    pass