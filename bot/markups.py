from aiogram import types

import translates


async def get_start_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(translates.SEARCH_PRODUCT, translates.COMMIT_SOLD)
    return markup


async def get_sizes_markup(sizes: list) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True, row_width=1)
    pack_button = types.KeyboardButton(translates.SOLD_PACK)
    markup.add(pack_button)
    sizes = [types.KeyboardButton(f"Размер: {size[0]}\nКоличество: {size[1]}") for size in sizes]
    markup.add(*sizes)
    return markup


async def get_cancel_markup() -> types.InlineKeyboardMarkup:
    button = types.InlineKeyboardButton("Да", callback_data="cancel")
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    return markup


async def get_remove_keyboard() -> types.ReplyKeyboardRemove():
    return types.ReplyKeyboardRemove()
