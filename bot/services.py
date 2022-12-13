from typing import Optional, Union

import settings
import api_request
import translates


async def get_product(code: str) -> Optional[dict]:
    unused_fields = ["id"]
    url = settings.API_URL + f"products/{code}/?format=json"
    response_data = await api_request.get_product_data(url=url)
    if not response_data:
        return None
    return await translates.translate_product(data=response_data, unused_fields=unused_fields)


async def commit_sold(code: str, size: int, quantity: int) -> Union[dict, str]:
    url = settings.API_URL + f"products/commit_sold/{code}/"
    status_code, content = await api_request.update_sold(
        url=url,
        data={"size": size, "quantity": quantity}
    )
    if status_code == 200:
        return await translates.translate_product(data=content)
    elif status_code == 404:
        if content["detail"].startswith("Size"):
            return translates.SIZE_NOT_FOUND.substitute(size=size)
        elif content["detail"].startswith("Product"):
            return translates.PRODUCT_NOT_FOUND.substitute(code=code)
    elif status_code == 400:
        return translates.INVALID_SOLD_QUANTITY.substitute(content)
