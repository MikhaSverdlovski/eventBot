import asyncio
import logging
from aiogram.types import FSInputFile
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

from Config import Config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=Config.TELEGRAM_TOKEN, parse_mode="HTML")
# Диспетчер
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    photo = FSInputFile("Static/1.jpg")
    caption = (f"<B>Добрый день, {message.from_user.first_name}</b> \n\n"
               "Здесь вы можете записаться на ближайшее мероприятие\n\n"
               "Cписок команд:\n"
               "\n"
               "/start - Перезапустить бота\n"
               "/register - Пройти процедуру регистрации\n"
               "/help - Помощь")
    await message.answer_photo(photo, caption=caption)


@dp.message(Command("register"))
async def cmd_register(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
