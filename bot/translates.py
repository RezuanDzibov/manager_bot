from typing import Optional
from string import Template

import utils


FIELD_TRANSLATIONS = {
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

BOOL_TRANSLATIONS = {
    True: "Да",
    False: "Нет",
}

INVALID_SOLD_QUANTITY = Template(
    "Вы не можете продать $client_quantity штук так как существует только $initial_quantity штук размера $size у товара $product_name"
)

SIZE_NOT_FOUND = Template("Размер: $size не найден")
PRODUCT_NOT_FOUND = Template("Товар с артикулом: $code не найден")
CODE_INVALID_ANSWER = "Артикул должен состоять из 7 символов, букв латинского алфавита и цифр. Пример: 11DC5A1 или 11dc5a1"


async def translate_sizes(data: dict) -> list:
    to_return = list()
    for size in data:
        size_data = dict()
        for size_field_name, size_field_value in size.items():
            size_data[f"{FIELD_TRANSLATIONS[size_field_name]}"] = size_field_value
        to_return.append(size_data)
    return to_return


async def translate_product(data: dict, unused_fields: Optional[list] = None) -> dict:
    to_return = {}
    for field_name, field_value in data.items():
        if unused_fields and field_name in unused_fields:
            continue
        if field_name == "sizes":
            to_return["sizes"] = await translate_sizes(data=field_value)
            continue
        if field_name == "images":
            if field_value:
                images = await utils.process_images(images=field_value)
                to_return["images"] = images
            continue
        if isinstance(field_value, bool):
            field_value = BOOL_TRANSLATIONS[field_value]
        if field_name.endswith("price"):
            field_value = f"{field_value}₽"
        to_return[f"{FIELD_TRANSLATIONS[field_name]}"] = field_value
    return to_return

