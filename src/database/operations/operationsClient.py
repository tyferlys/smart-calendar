from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from src.api.pydanticTypes.client import ClientCreateRequest, ClientGetResponse, ClientUpdateRequest, \
    ClientUpdateResponse, ClientCreateResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Client


async def get_clients_database(offset: int, limit: int) -> List[ClientGetResponse]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_clients = await session.execute(select(Client).offset(offset).limit(limit))
                founded_clients = founded_clients.scalars().all()

                return [ClientGetResponse(id=founded_client.id,
                                          last_name=founded_client.last_name,
                                          first_name=founded_client.first_name,
                                          middle_name=founded_client.middle_name,
                                          phone=founded_client.phone,
                                          username=founded_client.username) for founded_client in founded_clients]
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")


async def get_client_database(phone: str) -> ClientGetResponse | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_client = await session.execute(select(Client).where(Client.phone == phone))
                founded_client = founded_client.scalars().all()

                if len(founded_client) > 0:
                    return ClientGetResponse(id=founded_client[0].id,
                                             last_name=founded_client[0].last_name,
                                             first_name=founded_client[0].first_name,
                                             middle_name=founded_client[0].middle_name,
                                             phone=founded_client[0].phone,
                                             username=founded_client[0].username)
                else:
                    return None
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")


async def create_client_database(clientRequest: ClientCreateRequest) -> ClientCreateResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                client = Client(last_name=clientRequest.last_name, first_name=clientRequest.first_name,
                                middle_name=clientRequest.middle_name, phone=clientRequest.phone, username=clientRequest.username)

                session.add(client)
                await session.commit()

                return ClientCreateResponse(
                    id=client.id,
                    last_name=client.last_name,
                    first_name=client.first_name,
                    middle_name=client.middle_name,
                    phone=client.phone,
                    username = clientRequest.username
                )
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при создании клиента")


async def update_client_database(client: ClientUpdateRequest) -> ClientUpdateResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                await session.execute(update(Client)
                                      .where(Client.phone == client.phone)
                                      .values(last_name=client.last_name,
                                              first_name=client.first_name,
                                              middle_name=client.middle_name,
                                              username=client.username))

                clientUpdated = await session.execute(select(Client).where(Client.phone == client.phone))
                clientUpdated = clientUpdated.scalars().first()

                await session.commit()

                return ClientUpdateResponse(
                    id=clientUpdated.id,
                    last_name=clientUpdated.last_name,
                    first_name=clientUpdated.first_name,
                    middle_name=clientUpdated.middle_name,
                    phone=clientUpdated.phone,
                    username=clientUpdated.username
                )
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при обновлении клиента")