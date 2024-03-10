from typing import List

from pydantic import BaseModel


class ClientGetResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    username: str


class ClientGetAllResponse(BaseModel):
    clients: List[ClientGetResponse]
    count: int

class ClientCreateRequest(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    username: str


class ClientCreateResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    username: str


class ClientUpdateRequest(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    username: str


class ClientUpdateResponse(ClientUpdateRequest):
    pass
