from sqlalchemy import select, update

from src.api.pydanticTypes.owner import OwnerGetResponse, OwnerCreateRequest
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Owner


async def get_owner_database() -> OwnerGetResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                owner = await session.execute(select(Owner))
                owner = owner.scalars().first()

                return OwnerGetResponse(
                    id=owner.id,
                    last_name=owner.last_name,
                    first_name=owner.first_name,
                    middle_name=owner.middle_name,
                    phone=owner.phone,
                    password=owner.password
                )
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при получении владельца")


async def update_owner_database(owner: OwnerCreateRequest):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                await session.execute(update(Owner)
                                      .values(last_name=owner.last_name,
                                              first_name=owner.first_name,
                                              middle_name=owner.middle_name,
                                              phone=owner.phone,
                                              password=owner.password))

                await session.commit()
            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при обновлении клиента")