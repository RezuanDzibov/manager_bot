from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import md
import services
import states
import translates
import filters
from markups import get_sizes_markup
from settings import dp, bot
from utils import get_size_from_text
from handlers.utils import cancel, check_invalid_sizes, send_start_markup


@dp.message_handler(Text(contains=translates.COMMIT_SOLD), state=states.StartState)
async def process_commit_sold(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SoldCommitState.code.set()
    await message.reply("Введите артикул товара")
    await cancel(chat_id=message.chat.id)


@dp.message_handler(filters.validate_is_product_exists, state=states.SoldCommitState.code)
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
        await cancel(chat_id=message.chat.id)


@dp.message_handler(
    filters.validate_size_choice,
    state=states.SoldCommitState.size
)
async def process_sold_commit_size_invalid(message: types.Message):
    return await message.reply(
        "Вы не выбрали из предложенного списка"
    )


@dp.message_handler(state=states.SoldCommitState.size)
async def process_sold_commit_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == translates.SOLD_PACK:
            invalid_sizes = await check_invalid_sizes(sizes=data["sizes"])
            if invalid_sizes:
                await bot.send_message(
                    message.chat.id,
                    f"Количество товара размеров: {''.join(invalid_sizes)} равна нулю",
                )
                return await send_start_markup(chat_id=message.chat.id)
            product = await services.sold_pack(code=data["code"])
            if isinstance(product, dict):
                product = await md.format_product_data(data=product)
                await bot.send_message(message.chat.id, product)
                await send_start_markup(chat_id=message.chat.id)
            else:
                await bot.send_message(message.chat.id, translates.SOLD_PACK_INVALID)
                await send_start_markup(chat_id=message.chat.id)
        else:
            data["size"] = await get_size_from_text(message.text)
            await states.SoldCommitState.next()
            await message.reply("Введите количество")
            await cancel(chat_id=message.chat.id)


@dp.message_handler(
    filters.validata_size_quantity,
    state=states.SoldCommitState.quantity
)
async def process_sold_commit_quantity_invalid(message: types.Message):
    await message.reply(
        "Количество должно быть числом и не меньше 0 и не быть больше чем присутствующее количество товара этого размера"
    )
    return await cancel(chat_id=message.chat.id)


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
        await send_start_markup(chat_id=message.chat.id)


__all__ = [
    "process_commit_sold",
    "process_sold_commit_code_invalid",
    "process_sold_commit_code",
    "process_sold_commit_size",
    "process_sold_commit_quantity",
    "process_sold_commit_size_invalid",
    "process_sold_commit_quantity_invalid",
]
