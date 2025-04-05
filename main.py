import asyncio
import logging
import sys
import requests
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = "7559845248:AAFg3exmH5T9mVs-EHigaRRXB15SUBuCz7M"

dp = Dispatcher()

class ConverterState(StatesGroup):
    convert_currency = State()
    convert_amount = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message, state : FSMContext) -> None:
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text = "USD ➡️ UZS"),
        KeyboardButton(text = "UZS ➡️ USD")
    ])
    await state.set_state(ConverterState.convert_currency)
    rkb = rkb.as_markup(resize_keyboard=True)
    await message.answer(
        text=f"Assalomu aleykum Currency converter botga xush kelibsiz \n Bot orqali quyidagi pul birliklarini convert qila olasiz",
        reply_markup=rkb)

@dp.message(ConverterState.convert_currency)
async def convert_currency_handler(message: Message, state : FSMContext) -> None:
    from_currency, to_currency = message.text.split(" ➡️ ")
    await state.update_data({
        "from_currency": from_currency,
        "to_currency": to_currency
    })

    await state.set_state(ConverterState.convert_amount)
    await message.answer(text='Convert qilinadigan miqdorni kiriting:')


@dp.message(ConverterState.convert_amount)
async def convert_amount_handler(message: Message, state : FSMContext) -> None:
    data = await state.get_data()
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    money = float(message.text)
    response = requests.get(f'https://open.er-api.com/v6/latest/{from_currency}')
    convert = response.json().get('rates').get(to_currency)
    await state.clear()
    await message.answer(f"Convert: {to_currency} -> {convert*money : .2f}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
