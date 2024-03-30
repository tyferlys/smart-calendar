import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status
from loguru import logger

from src.api.pydanticTypes.service import ServiceCreateRequest, ServiceCreateResponse, ServiceGetRequest
from src.database.operations.operationsServices import create_service_database, get_services_database

routerService = APIRouter()

load_dotenv()
token = os.getenv("TOKEN")


@routerService.get("", tags=["services.get"])
async def get_services(response: Response) -> List[ServiceGetRequest] | None:
    logger.info(f"Запрос на получение услуг")
    try:
        services = await get_services_database()
        logger.info(f"Получено услуг - {len(services)}")

        response.status_code = status.HTTP_200_OK
        return services
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerService.post("", tags=["services.post"])
async def create_service(service: ServiceCreateRequest, response: Response) -> ServiceCreateResponse | None:
    logger.info(f"Запрос на создание услуги: данные - {service}")
    try:
        newService = await create_service_database(service)
        logger.info(f"Услуга создана: данные - {newService}")
        response.status_code = status.HTTP_201_CREATED
        return newService
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None