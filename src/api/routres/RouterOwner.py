from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.owner import OwnerGetResponse, OwnerCreateRequest, OwnerCreateResponse
from src.database.operations.operationsOwner import get_owner_database, update_owner_database

routerOwner = APIRouter()


@routerOwner.get("", tags=["owner.get"])
async def get_owner(response: Response) -> OwnerGetResponse | None:
    try:
        owner = await get_owner_database()

        response.status_code = status.HTTP_200_OK
        return owner
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerOwner.put("", tags=["owner.put"])
async def update_owner(owner: OwnerCreateRequest, response: Response) -> OwnerCreateResponse:
    try:
        await update_owner_database(owner)
        response.status_code = status.HTTP_200_OK
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return owner
