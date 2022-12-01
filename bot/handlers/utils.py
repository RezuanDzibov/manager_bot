from aiogram import types

from settings import bot
import md


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

