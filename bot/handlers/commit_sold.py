from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import md
import services
import states
import translates
from filters import validate_size_choice, validata_size_quantity, validate_is_product_exists
from markups import get_start_markup, get_sizes_markup
from settings import dp, bot
from utils import get_size_from_text
from handlers.utils import cancel


@dp.message_handler(Text(contains=translates.COMMIT_SOLD), state=states.StartState)
async def process_commit_sold(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SoldCommitState.code.set()
    await message.reply("Введите артикул товара")
    await cancel(message=message)


@dp.message_handler(validate_is_product_exists, state=states.SoldCommitState.code)
async def process_sold_commit_code_invalid(message: types.Message):
    return await message.reply(translates.PRODUCT_NOT_FOUND.substitute(code=message.text))


@dp.message_handler(state=states.SoldCommitState.code)
async def process_sold_commit_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["code"] = message.text
        product = await services.get_product(code=message.text)
        if not product:
            await bot.send_message(message.chat.id, translates.PRODUCT_NOT_FOUND.substitute(code=message.text))
            await state.finish()
        await states.SoldCommitState.size.set()
        sizes = [list(size.values()) for size in product["sizes"]]
        data["sizes"] = sizes
        markup = await get_sizes_markup(sizes=sizes)
        await bot.send_message(message.from_id, "Введите размер", reply_markup=markup)
        await cancel(message=message)


@dp.message_handler(
    validate_size_choice,
    state=states.SoldCommitState.size
)
async def process_sold_commit_size_invalid(message: types.Message):
    return await message.reply(
        "Размер должен быть числом и не меньше 0"
    )


@dp.message_handler(state=states.SoldCommitState.size)
async def process_sold_commit_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["size"] = await get_size_from_text(message.text)
        await states.SoldCommitState.next()
        await message.reply("Введите количество")
        await cancel(message=message)


@dp.message_handler(
    validata_size_quantity,
    state=states.SoldCommitState.quantity
)
async def process_sold_commit_quantity_invalid(message: types.Message):
    return await message.reply(
        "Количество должно быть числом и не меньше 0 и не быть больше чем присутствующее количество товара этого размера"
    )


@dp.message_handler(state=states.SoldCommitState.quantity)
async def process_sold_commit_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["quantity"] = message.text
        await state.finish()
        data_values = list(data.values())
        data_values.pop(1)
        product = await services.commit_sold(*data_values)
        if isinstance(product, dict):
            product = await md.format_product_data(data=product)
        await bot.send_message(message.chat.id, product)
    await state.finish()
    markup = await get_start_markup()
    await states.StartState.choice.set()
    await bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)


__all__ = [
    "process_commit_sold",
    "process_sold_commit_code_invalid",
    "process_sold_commit_code",
    "process_sold_commit_size",
    "process_sold_commit_quantity",
    "process_sold_commit_size_invalid",
    "process_sold_commit_quantity_invalid",
]
