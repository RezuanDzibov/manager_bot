import logging

from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text

import states
from filters import validate_user
from markups import get_start_markup
from settings import dp, bot


async def on_shutdown(dispatcher: Dispatcher):
    dp.storage.close()


@dp.message_handler(validate_user)
async def check_user_id(message: types.Message):
    await message.reply("Вам не разрешено пользоваться этим ботом")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    markup = await get_start_markup()
    await states.StartState.choice.set()
    await message.reply("Выберите действие", reply_markup=markup)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f"Cancelling state {current_state}")
    await state.finish()
    markup = await get_start_markup()
    await message.reply("Отмена действия", reply_markup=markup)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_q(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f"Cancelling state {current_state}")
    await state.finish()
    await states.StartState.choice.set()
    markup = await get_start_markup()
    await bot.send_message(call.from_user.id, "Выберите действие", reply_markup=markup)


__all__ = [
    "cmd_start",
    "cancel_handler",
    "check_user_id",
    "cancel_q"
]
