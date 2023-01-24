from aiogram import types

import md
import states
from markups import get_cancel_markup, get_start_markup
from settings import bot, dp


async def send_start_markup(chat_id):
    state = dp.current_state()
    await state.finish()
    markup = await get_start_markup()
    await states.StartState.choice.set()
    return await bot.send_message(chat_id, "Выберите действие", reply_markup=markup)


async def show_product(message: types.Message, product: dict):
    if "images" in product:
        await bot.send_media_group(message.chat.id, media=product.pop("images"))
    product = await md.format_product_data(data=product)
    await bot.send_message(
        message.chat.id,
        product,
        parse_mode=types.ParseMode.HTML,
    )
    return


async def cancel(message: types.Message):
    cancel_markup = await get_cancel_markup()
    await bot.send_message(chat_id, "Отменить действие?", reply_markup=cancel_markup)


async def check_invalid_sizes(sizes: list):
    to_return = list()
    for size, size_quantity in sizes:
        if size_quantity == 0:
            to_return.append(str(size))
    return to_return
