from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import services
import states
import translates
from markups import get_start_markup
from .utils import show_product
from settings import dp, bot


@dp.message_handler(Text(contains=translates.SEARCH_PRODUCT), state=states.StartState)
async def process_search_product(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SearchState.code.set()
    await message.reply("Введите артикул товара")


@dp.message_handler(lambda message: len(message.text) != 7, state=states.SearchState.code)
async def process_search_product_code_invalid(message: types.Message):
    return await message.reply(translates.CODE_INVALID_ANSWER)


@dp.message_handler(state=states.SearchState)
async def process_search_by_code(message: types.Message, state: FSMContext):
    product = await services.get_product(code=message.text.upper())
    if not product:
        await bot.send_message(message.chat.id, translates.PRODUCT_NOT_FOUND.substitute(code=message.text))
        await state.finish()
        return
    await show_product(message, product)
    await state.finish()
    markup = await get_start_markup()
    await states.StartState.choice.set()
    await bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)


__all__ = [
    "process_search_product",
    "process_search_product_code_invalid",
    "process_search_by_code",
]
