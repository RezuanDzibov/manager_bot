from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import services
import states
import translates
from markups import get_start_markup
from .utils import show_product, cancel
from settings import dp, bot
from filters import validate_is_product_exists


@dp.message_handler(Text(contains=translates.SEARCH_PRODUCT), state=states.StartState)
async def process_search_product(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SearchState.code.set()
    await message.reply("Введите артикул товара")
    await cancel(chat_id=message.chat.id)


@dp.message_handler(validate_is_product_exists)
async def process_search_product_code_invalid(message: types.Message):
    return await message.reply(translates.PRODUCT_NOT_FOUND.substitute(code=message.text))


@dp.message_handler(state=states.SearchState)
async def process_search_by_code(message: types.Message, state: FSMContext):
    product = await services.get_product(code=message.text)
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
