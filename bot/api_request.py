from typing import Optional

import aiohttp


async def get_product_data(url: str, *args, **kwargs) -> Optional[dict]:
    async with aiohttp.ClientSession() as client:
        async with client.get(url, *args, **kwargs) as response:
            if response.status == 404:
                return None
            if response.status == 200:
                response_data = await response.json()
                return response_data


async def update_sold(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as client:
        async with client.patch(url, *args, **kwargs) as response:
            return response.status, await response.json()


async def add_product(url, *args, **kwargs):
    async with aiohttp.ClientSession() as client:
        async with client.post(url, *args, **kwargs) as response:
            return response.status, await response.json()


async def add_product_image(url, *args, **kwargs):
    async with aiohttp.ClientSession() as client:
        async with client.post(url, *args, **kwargs) as response:
            return response.status
