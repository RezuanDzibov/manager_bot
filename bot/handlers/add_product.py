from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import markups
import translates
import services
import states
from filters import validate_date, validate_sizes_match_pattern, validate_sizes_have_valid_sum, \
    validate_pack_quantity_less_than_quantity
from settings import dp, bot, MEDIAFILES_DIR
from .utils import show_product


@dp.message_handler(Text(contains=translates.ADD_PRODUCT), state=states.StartState)
async def process_add_product(message: types.Message, state: FSMContext):
    await state.finish()
    await states.ProductAddState.name.set()
    await message.reply("Введите название товара")


@dp.message_handler(
    lambda message: len(message.text) > 255 or len(message.text) < 3,
    state=states.ProductAddState.name
)
async def process_add_product_name_invalid(message: types.Message):
    return await message.reply(
        "Название товара не должно быть меньше 3 или больше 255 букв"
    )


@dp.message_handler(state=states.ProductAddState.name)
async def process_add_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
        await states.ProductAddState.next()
        await message.reply("Введите цвет")


@dp.message_handler(
    lambda message: len(message.text) > 50 or len(message.text) < 3,
    state=states.ProductAddState.color
)
async def process_add_product_color_invalid(message: types.Message):
    return await message.reply(
        "Цвет товара не должен быть меньше 3 или больше 50 букв"
    )


@dp.message_handler(state=states.ProductAddState.color)
async def process_add_product_color(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["color"] = message.text
        await states.ProductAddState.next()
        await message.reply("Введите количество")


@dp.message_handler(
    lambda message: not message.text.isdigit() or int(message.text) < 1,
    state=states.ProductAddState.quantity
)
async def process_add_product_quantity_invalid(message: types.Message):
    return await message.reply(
        "Количество должно быть числом и не меньше 0"
    )


@dp.message_handler(state=states.ProductAddState.quantity)
async def process_add_product_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["quantity"] = int(message.text)
        await states.ProductAddState.next()
        await message.reply("Введите количество пачек")


@dp.message_handler(
    lambda message: not message.text.isdigit() or int(message.text) < 1,
    state=states.ProductAddState.pack_quantity
)
async def process_add_product_pack_quantity_invalid(message: types.Message):
    return await message.reply(
        "Количество пачек должно быть числом и не меньше 0"
    )


@dp.message_handler(
    validate_pack_quantity_less_than_quantity,
    state=states.ProductAddState.pack_quantity
)
async def process_add_product_pack_quantity_invalid_less_than_quantity(message: types.Message):
    return await message.reply(
        "Количество пачек не должно быть больше чем количество товара"
    )


@dp.message_handler(state=states.ProductAddState.pack_quantity)
async def process_add_product_pack_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["pack_quantity"] = int(message.text)
        await states.ProductAddState.next()
        await message.reply("Введите оптовую цену")


@dp.message_handler(
    lambda message: not message.text.isdigit() or int(message.text) < 1,
    state=states.ProductAddState.wholesale_price
)
async def process_add_product_wholesale_price_invalid(message: types.Message):
    return await message.reply(
        "Оптовая цена должна быть числом и не меньше 0"
    )


@dp.message_handler(state=states.ProductAddState.wholesale_price)
async def process_add_product_wholesale_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["wholesale_price"] = message.text
        await states.ProductAddState.next()
        await message.reply("Введите розничную цену")


@dp.message_handler(
    lambda message: not message.text.isdigit() or int(message.text) < 1,
    state=states.ProductAddState.retail_price
)
async def process_add_product_retail_price_invalid(message: types.Message):
    return await message.reply(
        "Розничная цена должна быть числом и не меньше 0"
    )


@dp.message_handler(state=states.ProductAddState.retail_price)
async def process_add_product_retail_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["retail_price"] = message.text
        await states.ProductAddState.next()
        await message.reply("Введите дату поставки. Пример: 31.06.22")


@dp.message_handler(
    validate_date,
    state=states.ProductAddState.supply_date
)
async def process_add_product_supply_date_invalid(message: types.Message):
    return await message.reply(
        "Дата поставки должна быть в виде: 31.06.22"
    )


@dp.message_handler(state=states.ProductAddState.supply_date)
async def process_add_product_supply_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        date = message.text.split(".")
        date.append("20" + date.pop(-1))
        data["supply_date"] = "-".join(reversed(date))
        await states.ProductAddState.next()
        await message.reply("Введите размеры. Пример: 130-20 140-30")


@dp.message_handler(
    validate_sizes_match_pattern,
    state=states.ProductAddState.sizes
)
async def process_add_product_sizes_invalid_by_pattern(message: types.Message, state: FSMContext):
    return await message.reply(
        "Резмеры должны быть в виде размер-количество резеделенные пробелами: 130-20 140-30"
    )


@dp.message_handler(
    validate_sizes_have_valid_sum,
    state=states.ProductAddState.sizes
)
async def process_add_product_sizes_invalid_by_sum(message: types.Message, state: FSMContext):
    return await message.reply(
        "Сумма количества размеров должна быть равна количеству товара"
    )


@dp.message_handler(state=states.ProductAddState.sizes)
async def process_add_product_sizes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sizes"] = [
            {"value": size_data.split("-")[0], "quantity": size_data.split("-")[1]}
            for size_data in message.text.split(" ")
        ]
        data["sold"] = 0
        data["remainder"] = data["quantity"]
        await states.ProductAddState.next()
        product = await services.add_product(data=dict(data))
        await show_product(message, product)
        markup = await markups.get_image_markup(product_code=product["Артикул"], first_call=True)
        await bot.send_message(message.chat.id, "Хотите добавить изображение/я к этому товару?", reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(markups.product_images_add_cb.filter(action="add_image"))
async def process_add_image_accept(call: types.CallbackQuery, callback_data: dict):
    await call.message.reply("Пожайлуста, используйте не сжатое изображение")
    await states.ProductAddImagesState.image.set()
    state = dp.current_state()
    async with state.proxy() as data:
        data["product_code"] = callback_data["product_code"]


@dp.callback_query_handler(text="not_add_image")
async def process_add_image_refuse(call: types.CallbackQuery):
    await call.message.reply("Ок")
    return


@dp.message_handler(content_types=["document"], state=states.ProductAddImagesState.image)
async def process_add_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        product_code = data["product_code"]
    await state.finish()
    image = message.document
    await image.download(destination_file=MEDIAFILES_DIR / image["file_name"])
    await services.add_product_image(filename=image["file_name"], product_code=product_code)
    markup = await markups.get_image_markup(product_code=product_code)
    await bot.send_message(message.chat.id, "Хотите добавить еще изоброжение?", reply_markup=markup)


__all__ = [
    "process_add_product",
    "process_add_product_name_invalid",
    "process_add_product_name",
    "process_add_product_color_invalid",
    "process_add_product_color",
    "process_add_product_quantity_invalid",
    "process_add_product_quantity",
    "process_add_product_pack_quantity_invalid",
    "process_add_product_pack_quantity_invalid_less_than_quantity",
    "process_add_product_pack_quantity",
    "process_add_product_wholesale_price_invalid",
    "process_add_product_wholesale_price",
    "process_add_product_retail_price_invalid",
    "process_add_product_retail_price",
    "process_add_product_supply_date_invalid",
    "process_add_product_supply_date",
    "process_add_product_sizes_invalid_by_pattern",
    "process_add_product_sizes_invalid_by_sum",
    "process_add_product_sizes",
    "process_add_image_accept",
    "process_add_image_refuse",
    "process_add_image",
]
