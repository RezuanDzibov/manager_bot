import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


BASE_DIR = Path(__file__).resolve().parent
MEDIAFILES_DIR = BASE_DIR.parent / "mediafiles"

load_dotenv(find_dotenv())

API_URL = str(os.environ.get("API_URL"))
API_TOKEN = str(os.environ.get("BOT_API_TOKEN"))

API_AUTH_USERNAME = str(os.environ.get("API_AUTH_USERNAME"))
API_AUTH_PASSWORD = str(os.environ.get("API_AUTH_PASSWORD"))

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
