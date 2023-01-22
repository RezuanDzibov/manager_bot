from aiogram import types

import md
from markups import get_cancel_markup
from settings import bot


async def show_product(message: types.Message, product: dict):
    if "images" in product:
        await bot.send_media_group(message.chat.id, media=product.pop("images"))
    product = await md.format_product_data(data=product)
    await bot.send_message(
        message.chat.id,
        product,
        parse_mode=types.ParseMode.MARKDOWN,
    )
    return


async def cancel(message: types.Message):
    cancel_markup = await get_cancel_markup()
    await bot.send_message(message.from_id, "Отменить действие?", reply_markup=cancel_markup)
