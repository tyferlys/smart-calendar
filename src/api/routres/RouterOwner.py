import os

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status
from loguru import logger

from src.api.pydanticTypes.owner import OwnerLoginResponse, OwnerUpdateRequest, OwnerLoginRequest, OwnerUpdateResponse
from src.database.operations.operationsOwner import update_owner_database, login_owner_database

routerOwner = APIRouter()

load_dotenv()
token = os.getenv("TOKEN")


@routerOwner.post("/login", tags=["owner.post"])
async def login_owner(password: OwnerLoginRequest, response: Response) -> OwnerLoginResponse | None:
    logger.info(f"Запрос на авторизацию администратора: пароль - {password}")
    try:
        owner = await login_owner_database(password.password)
        logger.info(f"Результат авторизации - {owner}")

        if owner is not None:
            response.status_code = status.HTTP_200_OK
            return owner
        else:
            response.status_code = status.HTTP_409_CONFLICT
            return None
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None


@routerOwner.put("", tags=["owner.put"])
async def update_owner(owner: OwnerUpdateRequest, response: Response) -> OwnerUpdateResponse | None:
    logger.info(f"Запрос на обновление данных администратора: данные - {owner}")
    try:
        newOwner = await update_owner_database(owner)
        logger.info(f"Администратор обновился: данные - {newOwner}")
        response.status_code = status.HTTP_200_OK
        return newOwner
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None
