import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status

from src.api.pydanticTypes.service import ServiceCreateRequest, ServiceCreateResponse, ServiceGetRequest
from src.database.operations.operationsServices import create_service_database, get_services_database

routerService = APIRouter()

load_dotenv()
token = os.getenv("TOKEN")


@routerService.get("", tags=["services.get"])
async def get_services(tokenRequest: str, response: Response) -> List[ServiceGetRequest]:
    try:
        if tokenRequest != token:
            response.status_code = status.HTTP_409_CONFLICT
            return []

        services = await get_services_database()

        response.status_code = status.HTTP_200_OK
        return services
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return []

@routerService.post("", tags=["services.post"])
async def create_service(tokenRequest: str, service: ServiceCreateRequest, response: Response) -> ServiceCreateResponse | None:
    try:
        if tokenRequest != token:
            response.status_code = status.HTTP_409_CONFLICT
            return None

        newService = await create_service_database(service)
        response.status_code = status.HTTP_201_CREATED
        return newService
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None