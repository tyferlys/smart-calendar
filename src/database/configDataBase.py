from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

import configProject

settings = configProject.get_settings()

DATABASE_URL = settings.PROD_DB_URL if settings.MODE == 'prod' else settings.DEV_DB_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
