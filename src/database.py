from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.config import URL

engine = create_async_engine(
    url=URL,
    echo=True
)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

async def async_main():
    async with engine.begin() as conn:
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++1')
        print(Base.metadata.tables)
        await conn.run_sync(Base.metadata.create_all)