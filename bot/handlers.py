import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import options
import states
import services
import markdown
from settings import dp, bot


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(options.SEARCH_PRODUCT)
    await states.StartState.choice.set()
    await message.reply("Выбирете действие", reply_markup=markup)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f"Cancelling state {current_state}")
    await state.finish()
    await message.reply("Отмена действия")


@dp.message_handler(Text(contains=options.SEARCH_PRODUCT), state=states.StartState)
async def process_search_product(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SearchState.code.set()
    await message.reply("Введите артикул товара")


@dp.message_handler(lambda message: len(message.text) != 7, state=states.SearchState.code)
async def process_code_invalid(message: types.Message):
    return await message.reply(
        "Артикул должен состоять из 7 символов, букв латинского алфавита и цифр. Пример: 11DC5A1 или 11dc5a1"
    )


@dp.message_handler(state=states.SearchState)
async def process_search_by_code(message: types.Message, state: FSMContext):
    product = await services.get_product(code=message.text.upper())
    if not product:
        await bot.send_message(message.chat.id, f"Такого товара с артикулом: {message.text} не найдено.")
        await state.finish()
        return
    if "images" in product:
        await bot.send_media_group(message.chat.id, media=product.pop("images"))
    product = await markdown.format_product_data(data=product)
    await bot.send_message(
        message.chat.id,
        product,
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await state.finish()
    return


__all__ = ["cmd_start", "cancel_handler", "process_search_product", "process_search_by_code"]
