from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

import configProject

DATABASE_URL = f"postgresql+asyncpg://{configProject.DB_USER}:{configProject.DB_PASS}@{configProject.DB_HOST}:{configProject.DB_PORT}/{configProject.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

