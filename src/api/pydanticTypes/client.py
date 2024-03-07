from pydantic import BaseModel


class ClientCreateRequest(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    phone: str


class ClientCreateResponse(ClientCreateRequest):
    pass


class ClientGetResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str