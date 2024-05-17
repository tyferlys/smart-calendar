from sqlalchemy import or_, select, update

from src.api.pydanticTypes.optionClient import OptionClientGetResponse, OptionClientUpdateRequest, \
    OptionClientUpdateResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Client, OptionsClient
from loguru import logger

async def get_option_client_database(phoneOrTelegramId: str) -> OptionClientGetResponse | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_client = await session.execute(select(Client).where(or_(Client.phone == phoneOrTelegramId, Client.telegram_id == phoneOrTelegramId)))
                founded_client = founded_client.scalars().first()
                if founded_client is None:
                    return None

                founded_option = await session.execute(select(OptionsClient).where(OptionsClient.id_client == founded_client.id))
                founded_option = founded_option.scalars().first()

                return OptionClientGetResponse(
                    id=founded_option.id,
                    id_client=founded_option.id_client,
                    is_notification=founded_option.is_notification,
                    timezone=founded_option.timezone
                )
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")


async def update_option_client_database(optionClient: OptionClientUpdateRequest) -> OptionClientUpdateResponse | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                await session.execute(update(OptionsClient).where(OptionsClient.id_client == optionClient.id_client).values(
                    id_client=optionClient.id_client,
                    is_notification=optionClient.is_notification,
                    timezone=optionClient.timezone
                ))

                founded_option = await session.execute(select(OptionsClient).where(OptionsClient.id_client == optionClient.id_client))
                founded_option = founded_option.scalars().first()

                await session.commit()

                return OptionClientUpdateResponse(
                    id=founded_option.id,
                    id_client=founded_option.id_client,
                    is_notification=founded_option.is_notification,
                    timezone=founded_option.timezone
                )
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")