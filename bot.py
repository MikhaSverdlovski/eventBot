import asyncio
import logging
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message
#Импортировать конфиги
from Config import Config


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=Config.Telegram_TOKEN)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


# Получение фото
@dp.message(F.photo)
async def echo_gif(message: Message):
    photo_id = message.photo[-1].file_id
    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path
    photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

    # Скачиваем фото временно
    photo_name = file_path.split('/')[-1]
    with requests.get(photo_url, stream=True) as r:
        with open(photo_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Загружаем фото на Яндекс.Диск
    if upload_file_to_yandex_disk(Config.YandexDisc_TOKEN, photo_name):
        await message.answer("Фотография успешно загружена на Яндекс.Диск")
        os.remove(photo_name)
    else:
        await message.answer("Не удалось загрузить фотографию на Яндекс.Диск")


def upload_file_to_yandex_disk(YandexDisc_TOKEN, file_path):
    headers = {'Authorization': f'OAuth {YandexDisc_TOKEN}'}

    # Указываем путь к папке на Яндекс.Диске
    yandex_disk_folder_path = "/TGBOT/"

    # Получаем ссылку для загрузки
    response = requests.get(
        'https://cloud-api.yandex.net/v1/disk/resources/upload',
        headers=headers,
        params={'path': yandex_disk_folder_path + os.path.basename(file_path), 'overwrite': 'true'}
    )
    href = response.json()['href']

    # Загружаем файл
    with open(file_path, 'rb') as file:
        requests.put(href, files={'file': file})

    return True


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
