from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import default_state

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]
available_food_names = ["Суши", "Спагетти", "Хачапури"]

kb_avail_food_names = [
    [types.KeyboardButton(text=size)] for size in available_food_names
]

kb_avail_food_sizes = [
    [types.KeyboardButton(text=size)] for size in available_food_sizes
]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


@router.message(Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_avail_food_names,
        resize_keyboard=True,
        input_field_placeholder="Выберите блюдо"
    )
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=keyboard
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_food_name)


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_avail_food_sizes,
        resize_keyboard=True,
        input_field_placeholder="Выберите блюдо"
    )
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=keyboard
    )
    await state.set_state(OrderFood.choosing_food_size)


@router.message(StateFilter("OrderFood:choosing_food_name"))
async def food_chosen_incorrectly(message: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_avail_food_names,
        resize_keyboard=True,
        input_field_placeholder="Выберите блюдо"
    )
    await message.answer(
        text="Я не знаю такого блюда.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=keyboard
    )


@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_avail_food_sizes,
        resize_keyboard=True,
        input_field_placeholder="Выберите блюдо"
    )
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=keyboard
    )

@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
