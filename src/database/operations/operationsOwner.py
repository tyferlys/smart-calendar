from sqlalchemy import select, update

from src.api.pydanticTypes import owner
from src.api.pydanticTypes.owner import OwnerLoginResponse, OwnerUpdateResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Owner


async def login_owner_database(password: str) -> OwnerLoginResponse | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                owner = await session.execute(select(Owner).where(Owner.password == password))
                owner = owner.scalars().all()

                if len(owner) > 0:
                    return OwnerLoginResponse(
                        id=owner[0].id,
                        last_name=owner[0].last_name,
                        first_name=owner[0].first_name,
                        middle_name=owner[0].middle_name,
                        phone=owner[0].phone,
                        password=owner[0].password,
                        token=owner[0].token
                    )
                else:
                    return None
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при получении владельца")


async def update_owner_database(owner: OwnerUpdateResponse):
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