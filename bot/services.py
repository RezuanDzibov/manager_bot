from typing import Optional

import settings
import utils
import api_request


field_translations = {
    "name": "Название",
    "code": "Артикул",
    "color": "Цвет",
    "pack_quantity": "Количество пачек",
    "wholesale_price": "Оптовая Цена",
    "retail_price": "Розничная Цена",
    "supply_date": "Дата поставки",
    "sold": "Продано",
    "remainder": "Остаток",
    "defective": "Брак",
    "refund": "Возврат",
    "quantity": "Количество",
    "sizes": "Размеры",
    "size_value": "Размер",
    "size_quantity": "Количество товаров размера"
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
        if field_name == "sizes":
            sizes = list()
            for size in field_value:
                size_data = dict()
                for size_field_name, size_field_value in size.items():
                    size_data[f"{field_translations[size_field_name]}"] = size_field_value
                sizes.append(size_data)
            to_return["sizes"] = sizes
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
