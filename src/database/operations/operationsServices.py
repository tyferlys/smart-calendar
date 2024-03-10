from typing import List

from sqlalchemy import select

from src.api.pydanticTypes.service import ServiceCreateRequest, ServiceCreateResponse, ServiceGetRequest
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Service


async def get_services_database() -> List[ServiceGetRequest]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_services = await session.execute(select(Service))
                founded_services = founded_services.scalars().all()

                return [ServiceGetRequest(id=founded_service.id,
                                          title=founded_service.title,
                                          cost=founded_service.cost,
                                          duration=founded_service.duration,
                                          after_pause=founded_service.after_pause) for founded_service in founded_services]
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")


async def create_service_database(serviceRequest: ServiceCreateRequest) -> ServiceCreateResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                service = Service(title=serviceRequest.title, cost=serviceRequest.cost, duration=serviceRequest.duration, after_pause=serviceRequest.after_pause)

                session.add(service)
                await session.commit()

                return ServiceCreateResponse(
                    id=service.id,
                    title=serviceRequest.title,
                    cost=serviceRequest.cost,
                    duration=serviceRequest.duration,
                    after_pause=serviceRequest.after_pause
                )
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при создании услуги")