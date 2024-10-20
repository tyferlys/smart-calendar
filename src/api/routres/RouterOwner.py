import os

from dotenv import load_dotenv
from fastapi import APIRouter, Response, status
from sqlalchemy import select, update
from loguru import logger

from src.api.pydanticTypes.owner import OwnerLoginResponse, OwnerUpdateRequest, OwnerLoginRequest, OwnerUpdateResponse
from src.database.models.models import Owner
from src.database.operations.operationsOwner import update_owner_database, login_owner_database
from src.database.configDataBase import AsyncSessionLocal
from configProject import get_settings
routerOwner = APIRouter()

load_dotenv()
settings = get_settings()
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


@routerOwner.get("/check_token", tags=["owner.get"])
async def check_owner_token(token: str, response: Response) -> OwnerLoginResponse | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                result = await session.execute(select(Owner).where(Owner.token == token))
                owner = result.scalars().first()

                if owner:
                    return OwnerLoginResponse(
                        id=owner.id,
                        last_name=owner.last_name,
                        first_name=owner.first_name,
                        middle_name=owner.middle_name,
                        phone=owner.phone,
                        password=owner.password,
                        token=owner.token
                    )
                else:
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                    return {"detail": "Токен недействителен или отсутствует"}
            except Exception as e:
                await session.rollback()
                isError = True
                logger.warning(f"Ошибка при проверке токена: {e}")
            finally:
                await session.close()

            if isError:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"detail": "Внутренняя ошибка сервера"}