from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import configProject
from src.database.configDataBase import Base

from src.database.models.models import Day, Service, Client, Event, Owner, Options

config = context.config
section = config.config_ini_section
settings = configProject.get_settings()

DATABASE_URL = settings.PROD_DB_URL if settings.MODE == 'prod' else settings.DEV_DB_URL
config.set_main_option('sqlalchemy.url', DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = config.attributes.get('async_engine')
    if connectable is None:
        connectable = create_async_engine(
            config.get_main_option('sqlalchemy.url'),
            poolclass=pool.NullPool,
        )
        config.attributes['async_engine'] = connectable

    async def async_main():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    import asyncio
    asyncio.run(async_main())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
