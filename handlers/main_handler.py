from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import FSInputFile
from aiogram import types, Router
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    photo = FSInputFile("Static/1.jpg")
    caption = (f"<B>Добрый день, {message.from_user.first_name}</b> \n\n"
               "Здесь Вы можете записаться на ближайшее мероприятие\n\n"
               "Cписок команд:\n"
               "\n"
               "/start - Перезапустить бота\n"
               "/register - Пройти процедуру регистрации\n"
               "/help - Помощь")
    await message.answer_photo(photo, caption=caption)

