
import functools
from aiogram import types

from Config import Config


# Импортировать конфиги


async def get_chat(message: types.Message):
    """Получение моего чат айди"""
    my_id = message.from_user.id
    return my_id


def check_user(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Получаем объект message из аргументов
        message = args[0]
        if message:  # Проверяем, существует ли объект message
            mychat_id = await get_chat(message)
            conf = Config.Chat_id
            if str(mychat_id) == conf:
                return await func(*args, **kwargs)
            else:
                return await message.answer("Свяжитесь с Михаилом Свердловским. Приложение только для него")
        else:
            raise ValueError("Argument 'message' is required for check_user decorator")

    return wrapper
