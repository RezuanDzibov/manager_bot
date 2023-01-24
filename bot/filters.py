from aiogram import types

import settings
import translates
from api_request import get_product_data
from settings import dp, ALLOWED_USERS
from utils import get_size_from_text


async def validate_size_choice(message: types.Message) -> bool:
    if message.text == translates.SOLD_PACK:
        return False
    state = dp.current_state()
    async with state.proxy() as data:
        try:
            size = int(await get_size_from_text(message.text))
            if size not in [size[0] for size in data["sizes"]]:
                return True
            return False
        except ValueError:
            return True


async def validata_size_quantity(message: types.Message) -> bool:
    try:
        quantity_from_message = int(message.text)
        if quantity_from_message <= 0:
            return True
    except ValueError:
        return True
    state = dp.current_state()
    async with state.proxy() as data:
        for size in data["sizes"]:
            if int(data["size"]) == size[0]:
                if quantity_from_message > size[1]:
                    return True
                return False
            else:
                continue
        return True


async def validate_user(message: types.Message) -> bool:
    if message.from_id in ALLOWED_USERS:
        return False
    return True


async def validate_is_product_exists(message: types.Message):
    url = settings.API_URL + f"products/{message.text}/?format=json"
    if await get_product_data(url=url):
        return False
    return True
