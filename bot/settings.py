import os
from pathlib import Path

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv, find_dotenv

BASE_DIR = Path(__file__).resolve().parent
MEDIAFILES_DIR = BASE_DIR.parent / "mediafiles"

load_dotenv(find_dotenv())

API_URL = str(os.environ.get("API_URL"))
API_TOKEN = str(os.environ.get("BOT_API_TOKEN"))

API_AUTH_USERNAME = str(os.environ.get("API_AUTH_USERNAME"))
API_AUTH_PASSWORD = str(os.environ.get("API_AUTH_PASSWORD"))
ALLOWED_USERS = [int(id_) for id_ in str(os.environ.get("ALLOWED_USERS")).split(" ")]
REDIS_HOST = str(os.environ.get("REDIS_HOST"))
REDIS_PORT = int(os.environ.get("REDIS_PORT"))

bot = Bot(token=API_TOKEN)
storage = RedisStorage2(REDIS_HOST, REDIS_PORT)
dp = Dispatcher(bot, storage=storage)
AUTH = aiohttp.BasicAuth(login=API_AUTH_USERNAME, password=API_AUTH_PASSWORD)
