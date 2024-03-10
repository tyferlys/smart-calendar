from pydantic import BaseModel


class ServiceGetRequest(BaseModel):
    id: int
    title: str
    cost: int
    duration: int
    after_pause: int


class ServiceCreateRequest(BaseModel):
    title: str
    cost: int
    duration: int
    after_pause: int


class ServiceCreateResponse(BaseModel):
    id: int
    title: str
    cost: int
    duration: int
    after_pause: int