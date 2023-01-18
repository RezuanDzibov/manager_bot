import logging

from aiogram import types

import settings


async def process_images(images: list) -> list:
    to_return = list()
    for image in images:
        image_path = str(settings.MEDIAFILES_DIR / image.split("/")[-1])
        try:
            to_return.append(types.InputMediaPhoto(types.InputFile(image_path)))
        except FileNotFoundError:
            logging.info(f"Not found media file {image.split('/')[-1]}")
    return to_return


async def get_size_from_text(message_text: str) -> str:
    return message_text.split("\n")[0].split(":")[1].strip()
