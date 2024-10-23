from typing import List
from sqlalchemy import select, delete
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


# Новый метод для удаления сервиса по ID
async def delete_service_by_id(service_id: int) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                # Находим сервис по ID
                result = await session.execute(select(Service).filter_by(id=service_id))
                service_to_delete = result.scalars().first()

                if not service_to_delete:
                    raise Exception(f"Сервис с ID {service_id} не найден")

                # Удаляем найденный сервис
                await session.delete(service_to_delete)
                await session.commit()

            except Exception as e:
                await session.rollback()
                isError = True
                print(f"Ошибка при удалении сервиса: {e}")
            finally:
                await session.close()

            if isError:
                raise Exception("Ошибка при удалении сервиса")