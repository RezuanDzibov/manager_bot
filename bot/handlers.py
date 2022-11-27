import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import options
import states
import services
import markdown
from settings import dp, bot
import translates


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(options.SEARCH_PRODUCT, options.COMMIT_SOLD)
    await states.StartState.choice.set()
    await message.reply("Выбирете действие", reply_markup=markup)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f"Cancelling state {current_state}")
    await state.finish()
    await message.reply("Отмена действия")


@dp.message_handler(Text(contains=options.SEARCH_PRODUCT), state=states.StartState)
async def process_search_product(message: types.Message, state: FSMContext):
    await state.finish()
    await states.SearchState.code.set()
    await message.reply("Введите артикул товара")


@dp.message_handler(lambda message: len(message.text) != 7, state=states.SearchState.code)
async def process_search_product_code_invalid(message: types.Message):
    return await message.reply(translates.CODE_INVALID_ANSWER)


@dp.message_handler(state=states.SearchState)
async def process_search_by_code(message: types.Message, state: FSMContext):
    product = await services.get_product(code=message.text.upper())
    if not product:
        await bot.send_message(message.chat.id, translates.PRODUCT_NOT_FOUND.substitute(code=message.text))
        await state.finish()
        return
    if "images" in product:
        await bot.send_media_group(message.chat.id, media=product.pop("images"))
    product = await markdown.format_product_data(data=product)
    await bot.send_message(
        message.chat.id,
        product,
        parse_mode=types.ParseMode.MARKDOWN,
    )
    await state.finish()
    return


@dp.message_handler(Text(contains=options.COMMIT_SOLD), state=states.StartState)
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
        "Размер должно быть числом и не меньше 0"
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
            product = await markdown.format_product_data(data=product)
        await bot.send_message(message.chat.id, product)


__all__ = [
    "cmd_start",
    "cancel_handler",
    "process_search_product",
    "process_search_product_code_invalid",
    "process_search_by_code",
    "process_commit_sold",
    "process_sold_commit_code_invalid",
    "process_sold_commit_code",
    "process_sold_commit_size",
    "process_sold_commit_quantity",
    "process_sold_commit_size_invalid",
    "process_sold_commit_quantity_invalid",
]
