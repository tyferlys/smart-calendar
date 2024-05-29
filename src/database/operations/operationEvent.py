import datetime
from typing import List

from loguru import logger
from sqlalchemy import select, insert, and_
from sqlalchemy.orm import joinedload

from src.api.pydanticTypes.record import RecordCreateRequest, RecordCreateResponse, RecordGetRequest
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Client, Service, Day, Options, Event, OptionsClient


async def get_records_client_database(phoneOrTelegramId: str) -> List[RecordGetRequest]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                client = await session.execute(select(Client).where(Client.telegram_id == phoneOrTelegramId))
                client = client.scalars().first()

                clientOption = await session.execute(select(OptionsClient).where(OptionsClient.id_client == client.id))
                clientOption = clientOption.scalars().first()

                events = await session.execute(
                    select(Event)
                    .where(and_(Event.id_client == client.id, Event.status == "wait"))
                    .options(joinedload(Event.service))
                    .options(joinedload(Event.day))
                    .order_by(Event.time)
                )
                events = events.scalars().all()

                timeDeltaClientTimeZone = datetime.timedelta(hours=clientOption.timezone)

                data = []
                for event in events:
                    data.append(RecordGetRequest(
                        date_day=event.day.date,
                        title_service=event.service.title,
                        time=(datetime.datetime.combine(event.day.date, event.time) + timeDeltaClientTimeZone).time()
                    ))

                return data
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при поиске записей")


async def create_record_database(event: RecordCreateRequest):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:
                client = await session.execute(select(Client).where(Client.telegram_id == event.telegram_id))
                client = client.scalars().first()

                clientOption = await session.execute(select(OptionsClient).where(OptionsClient.id_client == client.id))
                clientOption = clientOption.scalars().first()

                service = await session.execute(select(Service).where(Service.id == event.id_service))
                service = service.scalars().first()

                day = await session.execute(select(Day).where(Day.date == event.date_day))
                day = day.scalars().first()

                timeDeltaClientTimeZone = datetime.timedelta(hours=clientOption.timezone)
                timeClientEvent = datetime.datetime.combine(event.date_day, event.time) - timeDeltaClientTimeZone

                timeDeltaServiceDuration = datetime.timedelta(minutes=(service.duration + service.after_pause))
                timeClientEventEnd = datetime.datetime.combine(event.date_day, event.time) - timeDeltaClientTimeZone + timeDeltaServiceDuration

                if day is not None and day.status != "free":
                    similarEvents = await session.execute(select(Event).options(joinedload(Event.service)).options(joinedload(Event.client)).where(Event.id_day == day.id))
                    similarEvents = similarEvents.scalars().all()

                    for similarEvent in similarEvents:
                        timeDeltaDuration = datetime.timedelta(minutes=similarEvent.service.duration)
                        timeDeltaAfterPause = datetime.timedelta(minutes=similarEvent.service.after_pause)

                        beginTimeEvent = datetime.datetime.combine(day.date, similarEvent.time)
                        endTime = beginTimeEvent + timeDeltaDuration + timeDeltaAfterPause

                        if beginTimeEvent.time() < timeClientEvent.time() < endTime.time():
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

                if not (day.begin_time <= timeClientEvent.time() <= day.end_time):
                    logger.warning("День не входит во временные рамки рабочего дня")
                    return None

                newEvent = Event(
                    id_day=day.id,
                    id_service=service.id,
                    id_client=client.id,
                    status="wait",
                    time=timeClientEvent.time(),
                )
                session.add(newEvent)
                await session.commit()

                if timeClientEventEnd.time() >= day.end_time:
                    day.status = "closed"
                    session.add(day)
                    await session.commit()
                    logger.info("День заблокирован")

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

