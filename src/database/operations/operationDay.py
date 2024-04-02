import datetime
from typing import List

from loguru import logger
from sqlalchemy import select, and_, desc
from sqlalchemy.orm import joinedload

from src.api.pydanticTypes.day import DayGetResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Day, Event, Options


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


async def get_day_database(dateDay: datetime.date) -> DayGetResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                founded_day = await session.execute(select(Day).where(Day.date == dateDay))
                founded_day = founded_day.scalars().first()
                logger.info(f"Найден день - {founded_day}, {dateDay}")

                if founded_day is None:
                    option = await session.execute(select(Options))
                    option = option.scalars().first()

                    return DayGetResponse(
                        begin_time_free=option.begin_time,
                        end_time_free=option.end_time
                    )

                founded_event = await session.execute(select(Event).options(joinedload(Event.service)).where(Event.id_day == founded_day.id).order_by(desc(Event.time)))
                founded_event = founded_event.scalars().first()
                logger.info(f"Найдено последнее событие - {founded_event}")

                if founded_event is None:
                    return DayGetResponse(
                        begin_time_free=founded_day.begin_time,
                        end_time_free=founded_day.end_time
                    )

                timeDeltaDuration = datetime.timedelta(minutes=founded_event.service.duration)
                timeDeltaAfterPause = datetime.timedelta(minutes=founded_event.service.after_pause)

                begin_time_free = (datetime.datetime.combine(founded_day.date, founded_event.time) + timeDeltaDuration + timeDeltaAfterPause).time()

                return DayGetResponse(
                    begin_time_free=begin_time_free,
                    end_time_free=founded_day.end_time
                )
            except Exception as e:
                await session.rollback()
                print(e)
                isError = True
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске")
