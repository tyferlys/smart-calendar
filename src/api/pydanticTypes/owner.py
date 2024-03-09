from pydantic import BaseModel


class OwnerLoginRequest(BaseModel):
    password: str


class OwnerLoginResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    password: str
    token: str


class OwnerUpdateRequest(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    phone: str
    password: str


class OwnerUpdateResponse(OwnerUpdateRequest):
    pass
