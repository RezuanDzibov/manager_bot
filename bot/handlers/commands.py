import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import states
import settings
from settings import dp
from markups import get_start_markup


@dp.message_handler(lambda message: message.from_user.id not in settings.ALLOWED_USER_IDS)
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    markup = await get_start_markup()
    await states.StartState.choice.set()
    await message.reply("Выберите действие", reply_markup=markup)


@dp.message_handler(lambda message: message.from_user.id not in settings.ALLOWED_USER_IDS)
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f"Cancelling state {current_state}")
    await state.finish()
    await message.reply("Отмена действия")


__all__ = [
    "cmd_start",
    "cancel_handler",
]
