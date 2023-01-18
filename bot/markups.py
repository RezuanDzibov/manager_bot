from aiogram import types

import translates


async def get_start_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(translates.SEARCH_PRODUCT, translates.COMMIT_SOLD)
    return markup


async def get_sizes_markup(sizes: list) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True, row_width=1)
    sizes = [types.KeyboardButton(f"Размер: {size[0]}\nКоличество: {size[1]}") for size in sizes]
    markup.add(*sizes)
    return markup
