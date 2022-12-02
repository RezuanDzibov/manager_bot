from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import services
import states
from settings import dp, bot
import translates
import md


@dp.message_handler(Text(contains=translates.COMMIT_SOLD), state=states.StartState)
async def process_commit_sold(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SoldCommitState.code.set()
    await message.reply("Введите артикул товара")


@dp.message_handler(lambda message: len(message.text) != 7, state=states.SoldCommitState.code)
async def process_sold_commit_code_invalid(message: types.Message):
    return await message.reply(translates.CODE_INVALID_ANSWER)


@dp.message_handler(state=states.SoldCommitState.code)
async def process_sold_commit_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["code"] = message.text
        await states.SoldCommitState.next()
        await message.reply("Введите размер")


@dp.message_handler(
    lambda message: not message.text.isdigit() or int(message.text) < 1,
    state=states.SoldCommitState.size
)
async def process_sold_commit_size_invalid(message: types.Message):
    return await message.reply(
        "Размер должен быть числом и не меньше 0"
    )


@dp.message_handler(state=states.SoldCommitState.size)
async def process_sold_commit_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["size"] = message.text
        await states.SoldCommitState.next()
        await message.reply("Введите количество")


@dp.message_handler(
    lambda message: not message.text.isdigit() or int(message.text) < 1,
    state=states.SoldCommitState.quantity
)
async def process_sold_commit_quantity_invalid(message: types.Message):
    return await message.reply(
        "Количество должно быть числом и не меньше 0"
    )


@dp.message_handler(state=states.SoldCommitState.quantity)
async def process_sold_commit_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["quantity"] = message.text
        await state.finish()
        product = await services.commit_sold(*data.values())
        if isinstance(product, dict):
            product = await md.format_product_data(data=product)
        await bot.send_message(message.chat.id, product)


__all__ = [
    "process_commit_sold",
    "process_sold_commit_code_invalid",
    "process_sold_commit_code",
    "process_sold_commit_size",
    "process_sold_commit_quantity",
    "process_sold_commit_size_invalid",
    "process_sold_commit_quantity_invalid",
]
