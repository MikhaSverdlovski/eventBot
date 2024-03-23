import asyncio
import logging
from aiogram.types import FSInputFile
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from handlers import registration_handler, main_handler
from Config import Config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Объект бота
    bot = Bot(token=Config.TELEGRAM_TOKEN, parse_mode="HTML")
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(registration_handler.router, main_handler.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
