import os
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession


engine = create_async_engine('postgresql+asyncpg://postgres:2005@localhost:5432/postgres')
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