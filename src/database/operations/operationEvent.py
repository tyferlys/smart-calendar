import datetime
from typing import List

from loguru import logger
from sqlalchemy import select, insert, and_
from sqlalchemy.orm import joinedload

from src.api.pydanticTypes.record import RecordCreateRequest, RecordCreateResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Client, Service, Day, Options, Event


async def create_client_database(event: RecordCreateRequest):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                client = await session.execute(select(Client).where(Client.telegram_id == event.telegram_id))
                client = client.scalars().first()

                service = await session.execute(select(Service).where(Service.id == event.id_service))
                service = service.scalars().first()

                day = await session.execute(select(Day).where(Day.date == event.date_day))
                day = day.scalars().first()

                if client is None or service is None:
                    logger.warning("Клиента или услуги не существует")
                    raise Exception()

                if day is not None and day.status != "free":
                    similarEvents = await session.execute(select(Event).options(joinedload(Event.service)).where(Event.id_day == day.id))
                    similarEvents = similarEvents.scalars().all()

                    if len(similarEvents) != 0:
                        for similarEvent in similarEvents:
                            timeDeltaDuration = datetime.timedelta(minutes=similarEvent.service.duration)
                            timeDeltaAfterPause = datetime.timedelta(minutes=similarEvent.service.after_pause)

                            endTime = datetime.datetime.combine(day.date, similarEvent.time) + timeDeltaDuration + timeDeltaAfterPause
                            endTime = endTime.replace(tzinfo=similarEvent.time.tzinfo).timetz()

                            logger.info(endTime)
                            print(endTime)

                            if similarEvent.time <= event.time <= endTime:
                                logger.warning("Запись перекрывается другой")
                                return None
                elif day is not None and day.status == "free":
                    logger.warning("День выходной")
                    return None
                elif day is None:
                    option = await session.execute(select(Options))
                    options = option.scalars().first()

                    day = Day(date=event.date_day, status="have_event", begin_time=options.begin_time, end_time=options.end_time)
                    session.add(day)
                    await session.flush()

                if not (day.begin_time <= event.time <= day.end_time):
                    logger.warning("День не входит во временные рамки рабочего дня")
                    return None

                newEvent = Event(
                    id_day=day.id,
                    id_service=service.id,
                    id_client=client.id,
                    status="work",
                    time=event.time,
                )
                session.add(newEvent)
                await session.commit()

                logger.info(f"{client} \n {service} \n {day} \n {newEvent}")
                return newEvent
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при создании записи")

#TODO РАЗОБРАТЬСЯ С ТАЙМЗОНОЙ