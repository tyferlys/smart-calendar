from functools import lru_cache

from dotenv import load_dotenv
import os
from pydantic.v1 import BaseSettings
from dotenv import find_dotenv


class Settings(BaseSettings):
    DEV_DB_URL: str
    PROD_DB_URL: str
    MODE: str
    TOKEN: str

    class Config:
        env_file = find_dotenv(".env")


@lru_cache()
def get_settings():
    return Settings()
