import os
from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession


engine = create_async_engine(os.environ.get('URL_DB'))
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


#------------------Создание образа модели----------------------
class Base(AsyncAttrs, DeclarativeBase):
    pass


#------------------Создание модели для Пользователя----------------------
class UserMunSteam(Base):
    __tablename__ = 'UserMunSteam'
    telegram_id = Column(String, primary_key=True, unique=True)
    steam_id = Column(String, default=None)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)