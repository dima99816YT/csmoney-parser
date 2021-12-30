from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import json
import time
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'TOKEN'
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
catalog_types = {'ножи': 2, 'перчатки': 13, 'пистолеты': 5}


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Категории: ножи, перчатки, пистолеты')


@dp.message_handler(content_types=['text'])
async def get_category(message: types.Message):     # Baaaaad
    try:
        global catalog_type
        catalog_type = catalog_types[message.text]
        await message.answer('Введите количество страниц:')
    except:
        pages = int(message.text)
        collect_data(pages, catalog_type=catalog_type)
        with open('result.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("price")}'

            if index % 30 == 0:
                time.sleep(1)
            await message.answer(card)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
