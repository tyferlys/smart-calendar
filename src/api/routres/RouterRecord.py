import datetime

from fastapi import APIRouter

routerRecord = APIRouter()


# @routerRecord.get("", tags=["records.get"])
# async def get_records():
#     pass
#
#
# @routerRecord.get("/client", tags=["records.get"])
# async def get_records_client(phoneOrTelegramId: str):
#     pass
#
#
# @routerRecord.post("", tags=["records.post"])
# async def create_record():
#     pass
#
#
# @routerRecord.put("", tags=["records.put"])
# async def update_record():
#     pass
