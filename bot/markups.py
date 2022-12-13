from aiogram import types

import translates


async def get_start_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(translates.SEARCH_PRODUCT, translates.COMMIT_SOLD)
    return markup
