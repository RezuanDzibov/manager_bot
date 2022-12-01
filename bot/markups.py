from aiogram import types
from aiogram.utils.callback_data import CallbackData


product_images_add_cb = CallbackData("product_images_add", "action", "product_code")


async def get_image_markup(product_code: str, first_call: bool = False):
    markup = types.InlineKeyboardMarkup()
    add_image = types.InlineKeyboardButton(
        text="Добавить изображение",
        callback_data=product_images_add_cb.new(action="add_image", product_code=product_code)
    )
    not_add_images = types.InlineKeyboardButton(
        text="Нет" if first_call else "Этого достаточно",
        callback_data="not_add_image"
    )
    markup.add(add_image, not_add_images)
    return markup
