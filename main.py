import urllib.request
import xml.dom.minidom as minidom
import logging
from aiogram import Bot, Dispatcher, executor, types
from db import *
from auth_data import *

def get_data(xml_url):
    web_file = urllib.request.urlopen(xml_url)
    return web_file.read()


def get_currencies_dict(xml_cont):
    dom = minidom.parseString(xml_cont)
    dom.normalize()

    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict


def print_dict(dict):
    for i in dict.keys():
        print(i, dict[i])


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Бот для получения курсов валют\n\n"" \
         ")

@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = read_currencies_rates_from_db(db_path)
    await message.answer(answer_message)

@dp.message_handler(commands=['all'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = get_currencies_dict(get_data(url))
    await message.answer(answer_message)

if __name__ == '__main__':
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    db_path = './ currencies.db'
    currency_dict = get_currencies_dict(get_data(url))
    print_dict(currency_dict)
    write_currencies_to_db(currency_dict, db_path)
    print_currencies_list(read_currencies_rates_from_db(db_path))
    executor.start_polling(dp, skip_updates=True)
