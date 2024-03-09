from pydantic import BaseModel


class ClientGetResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str


class ClientCreateRequest(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    phone: str


class ClientCreateResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str


class ClientUpdateRequest(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str


class ClientUpdateResponse(ClientUpdateRequest):
    pass
