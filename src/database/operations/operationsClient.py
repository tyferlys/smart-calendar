from typing import List

from sqlalchemy import select, update, or_
from sqlalchemy.orm import joinedload

from src.api.pydanticTypes.client import ClientCreateRequest, ClientGetResponse, ClientUpdateRequest, \
    ClientUpdateResponse, ClientCreateResponse, ClientGetAllResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Client, OptionsClient


async def get_clients_database(offset: int, limit: int) -> ClientGetAllResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_clients = await session.execute(select(Client).offset(offset).limit(limit))
                founded_clients = founded_clients.scalars().all()
                count = await session.execute(select(Client))
                count = count.scalars().all()

                founded_clients = [ClientGetResponse(id=founded_client.id,
                                          last_name=founded_client.last_name,
                                          first_name=founded_client.first_name,
                                          middle_name=founded_client.middle_name,
                                          phone=founded_client.phone,
                                          username=founded_client.username,
                                          telegram_id=founded_client.telegram_id) for founded_client in founded_clients]
                count = len(count)

                return ClientGetAllResponse(
                    clients=founded_clients,
                    count=count
                )
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")


async def get_client_database(phoneOrTelegramId: str) -> ClientGetResponse | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_client = await session.execute(select(Client).where(or_(Client.phone == phoneOrTelegramId, Client.telegram_id == phoneOrTelegramId)))
                founded_client = founded_client.scalars().all()

                if len(founded_client) > 0:
                    return ClientGetResponse(id=founded_client[0].id,
                                             last_name=founded_client[0].last_name,
                                             first_name=founded_client[0].first_name,
                                             middle_name=founded_client[0].middle_name,
                                             phone=founded_client[0].phone,
                                             username=founded_client[0].username,
                                             telegram_id=founded_client[0].telegram_id)
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
                                middle_name=clientRequest.middle_name, phone=clientRequest.phone, username=clientRequest.username, telegram_id=clientRequest.telegram_id)
                session.add(client)
                await session.flush()

                clientOption = OptionsClient(id_client=client.id, is_notification=False, timezone=3)
                session.add(clientOption)

                await session.commit()

                return ClientCreateResponse(
                    id=client.id,
                    last_name=client.last_name,
                    first_name=client.first_name,
                    middle_name=client.middle_name,
                    phone=client.phone,
                    username=client.username,
                    telegram_id=client.telegram_id
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
                                              username=client.username,
                                              telegram_id=client.telegram_id))

                clientUpdated = await session.execute(select(Client).where(Client.phone == client.phone))
                clientUpdated = clientUpdated.scalars().first()

                await session.commit()

                return ClientUpdateResponse(
                    id=clientUpdated.id,
                    last_name=clientUpdated.last_name,
                    first_name=clientUpdated.first_name,
                    middle_name=clientUpdated.middle_name,
                    phone=clientUpdated.phone,
                    username=clientUpdated.username,
                    telegram_id=clientUpdated.telegram_id
                )
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при обновлении клиента")