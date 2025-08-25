import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']
SYNC_SQLALCHEMY_DATABASE_URL = os.environ['SYNC_DATABASE_URL']

sync_engine = create_engine(
    SYNC_SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
)

# Common pool settings for async engine
pool_settings = {
    "pool_size": 10,
    "max_overflow": 5,
    "pool_timeout": 30,
    "pool_recycle": 1800,
    "pool_pre_ping": True,
}

if os.environ.get('DEBUG') == 'True':
    async_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        **pool_settings
    )
else:
    async_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"ssl": "require"},
        **pool_settings
    )

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    future=True
)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()

metadata_obj = MetaData()


async def async_get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


def sync_get_db() -> Session:
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
