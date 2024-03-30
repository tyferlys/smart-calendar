from fastapi import APIRouter, Response, status
from loguru import logger

from src.api.pydanticTypes.report import ReportCreateRequest, ReportCreateResponse
from src.database.operations.operationsReport import create_report_database

routerReport = APIRouter()


@routerReport.post("", tags=["reports.post"])
async def create_report(report: ReportCreateRequest, response: Response) -> ReportCreateResponse | None:
    logger.info(f"Запрос на создание обращения: данные - {report}")
    try:
        newReport = await create_report_database(report)
        logger.info(f"Обращение создано: данные - {newReport}")
        response.status_code = status.HTTP_201_CREATED
        return newReport
    except Exception as e:
        logger.warning(f"Ошибка при выполнении запроса - {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return None
