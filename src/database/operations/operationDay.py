import datetime
from typing import List

from sqlalchemy import select, and_

from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Day


async def get_days_database(beginDate: datetime.date, endDate: datetime.date) -> List[int]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_days = await session.execute(select(Day).where(and_(Day.date >= beginDate, Day.date <= endDate, Day.status == "free")))
                founded_days = founded_days.scalars().all()

                return [
                    day.date.day for day in founded_days
                ]

            except Exception as e:
                await session.rollback()
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")
