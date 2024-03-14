from pydantic import BaseModel


class OptionClientGetResponse(BaseModel):
    id: int
    id_client: int
    is_notification: bool


class OptionClientUpdateRequest(BaseModel):
    id: int
    id_client: int
    is_notification: bool


class OptionClientUpdateResponse(OptionClientUpdateRequest):
    pass