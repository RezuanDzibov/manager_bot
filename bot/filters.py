import datetime
import re

from aiogram import types

from settings import dp


async def validate_pack_qunatity_less_than_qunatity(message: types.Message) -> bool:
    state = dp.current_state()
    async with state.proxy() as data:
        if int(message.text) <= data["quantity"]:
            return False
        return True


async def validate_date(message: types.Message) -> bool:
    try:
        datetime.datetime.strptime(message.text, "%d.%m.%y")
        return False
    except ValueError:
        return True


async def validate_sizes_match_pattern(message: types.Message) -> bool:
    pattern = "[1-9]?[0-9]+-[1-9]?[0-9]+"
    sizes = message.text.split(" ")
    if not sizes:
        return True
    if not all([re.match(pattern=pattern, string=size) for size in sizes]):
        return True
    return False


async def validate_sizes_have_valid_sum(message: types.Message) -> bool:
    sizes = message.text.split(" ")
    state = dp.current_state()
    async with state.proxy() as data:
        if sum(int(size.split("-")[1]) for size in sizes) == data["quantity"]:
            return False
        return True
