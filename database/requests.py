from database.models import User
from database.models import async_session
from sqlalchemy import select
from dataclasses import dataclass
import logging
from datetime import datetime

"""USER"""


async def get_user(tg_id: int) -> User:
    logging.info(f'get_user')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def add_user(tg_id: int, data: dict) -> None:
    """
    Добавляем нового пользователя если его еще нет в БД
    :param tg_id:
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # если пользователя нет в базе
        if not user:
            session.add(User(**data))
            await session.commit()


async def get_all_users() -> list[User]:
    """
    Получаем список всех пользователей зарегистрированных в боте
    :return:
    """
    logging.info(f'get_all_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        list_users = [user for user in users]
        return list_users


async def get_list_users() -> list:
    """
    ПОЛЬЗОВАТЕЛЬ - список пользователей верифицированных в боте
    :return:
    """
    logging.info(f'get_list_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        return [[user.tg_id, user.username] for user in users]
