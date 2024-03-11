from sqlalchemy import select

from src.api.pydanticTypes.report import ReportCreateRequest, ReportCreateResponse
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Client, Report


async def create_report_database(reportRequest: ReportCreateRequest) -> ReportCreateResponse:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            isError = False
            try:

                client = await session.execute(select(Client).where(Client.phone == reportRequest.phone))
                client = client.scalars().first()

                newReport = Report(
                    id_client=client.id,
                    text=reportRequest.text
                )
                session.add(newReport)
                await session.commit()

                return ReportCreateResponse(
                    id=client.id,
                    last_name=client.last_name,
                    first_name=client.first_name,
                    middle_name=client.middle_name,
                    phone=client.phone,
                    username=client.username,
                    text=reportRequest.text
                )
            except Exception as e:
                await session.rollback()
                isError = True
                print(e)
            finally:
                await session.close()

            if isError:
                raise Exception("ошибка при создании обращения")