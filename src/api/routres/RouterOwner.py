import os

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.owner import OwnerLoginResponse, OwnerUpdateRequest, OwnerLoginRequest, OwnerUpdateResponse
from src.database.operations.operationsOwner import update_owner_database, login_owner_database

routerOwner = APIRouter()

load_dotenv()
token = os.getenv("TOKEN")


@routerOwner.post("/login", tags=["owner.post"])
async def login_owner(password: OwnerLoginRequest, response: Response) -> OwnerLoginResponse | None:
    try:
        owner = await login_owner_database(password.password)

        if owner is not None:
            response.status_code = status.HTTP_200_OK
            return owner
        else:
            response.status_code = status.HTTP_409_CONFLICT
            return None
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerOwner.put("", tags=["owner.put"])
async def update_owner(owner: OwnerUpdateRequest, response: Response) -> OwnerUpdateResponse | None:
    try:
        newOwner = await update_owner_database(owner)
        response.status_code = status.HTTP_200_OK
        return newOwner
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None
