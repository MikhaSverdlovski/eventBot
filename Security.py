import asyncio
import functools
from datetime import datetime

import aiofiles
from aiogram import types

from Config import Config


# Импортировать конфиги


async def get_chat(message: types.Message):
    """Получение моего чат айди"""
    my_id = message.from_user.id
    return my_id


async def get_user(message: types.Message):
    try:
        username = message.from_user.username
        return username
    except Exception as e:
        print("Error:", e)
        return None


def check_user(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Получаем объект message из аргументов
        message = args[0]
        if message:  # Проверяем, существует ли объект message
            mychat_id = await get_chat(message)
            conf = Config.Chat_id
            if str(mychat_id) == conf:
                username = await get_user(message)
                await logging(chat_id=mychat_id, username=username)
                return await func(*args, **kwargs)
            else:
                await logging(chat_id=mychat_id, username=get_user(message))
                return await message.answer("Свяжитесь с Михаилом Свердловским. Приложение только для него")
        else:
            raise ValueError("Argument 'message' is required for check_user decorator")

    return wrapper


async def logging(chat_id: str, username: str) -> None:
    if username is not None:
        async with aiofiles.open("log.txt", "a") as f:
            await f.write(f"{datetime.datetime.now()} chat_id: {chat_id} Username: {username}\n")
