from aiogram import types

import settings


async def process_images(images: list) -> list:
    to_return = list()
    for image in images:
        image_path = str(settings.MEDIAFILES_DIR / image.split("/")[-1])
        to_return.append(types.InputMediaPhoto(types.InputFile(image_path)))
    return to_return
