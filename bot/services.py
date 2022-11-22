from typing import Optional

from aiogram.utils import markdown as md

import settings
import utils
import api_request


field_translations = {
    "name": "Название",
    "code": "Артикул",
    "wholesale_price": "Оптовая Цена",
    "retail_price": "Розничная Цена",
    "supply_date": "Дата поставки",
    "sale_date": "Дата продажи",
    "refund": "Возврат",
    "remainder": "Остаток",
    "quantity": "Количество",
    "size": "Размер",
    "color": "Цвет",
    "defective": "Брак",
}

bool_translations = {
    True: "Да",
    False: "Нет",
}


async def get_product(code: str) -> Optional[dict]:
    unused_fields = ["id"]
    url = settings.API_URL + f"products/{code}/?format=json"
    response_data = await api_request.get_product_data(url=url)
    if not response_data:
        return None
    to_return = {}
    for field_name, field_value in response_data.items():
        if field_name in unused_fields:
            continue
        if field_name == "images":
            if field_value:
                images = await utils.process_images(images=field_value)
                to_return["images"] = images
            continue
        if isinstance(field_value, bool):
            field_value = bool_translations[field_value]
        if field_name.endswith("price"):
            field_value = f"{field_value}₽"
        to_return[f"{field_translations[field_name]}"] = field_value
    return to_return
