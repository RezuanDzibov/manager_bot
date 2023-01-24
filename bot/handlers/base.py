import logging

from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text

from filters import validate_user
from handlers.utils import send_start_markup
from settings import dp


async def on_shutdown(dispatcher: Dispatcher):
    dp.storage.close()


@dp.message_handler(validate_user)
async def check_user_id(message: types.Message):
    await message.reply("Вам не разрешено пользоваться этим ботом")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await send_start_markup(chat_id=message.chat.id)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await send_start_markup(chat_id=message.chat.id)
    logging.info(f"Cancelling state {current_state}")
    await send_start_markup(chat_id=message.chat.id)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_q(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await send_start_markup(chat_id=call.from_user.id)
    logging.info(f"Cancelling state {current_state}")
    await send_start_markup(chat_id=call.from_user.id)


__all__ = [
    "cmd_start",
    "cancel_handler",
    "check_user_id",
    "cancel_q"
]
