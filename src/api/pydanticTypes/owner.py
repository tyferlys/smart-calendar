from pydantic import BaseModel


class OwnerGetResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    password: str


class OwnerCreateRequest(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    password: str


class OwnerCreateResponse(OwnerCreateRequest):
    pass
