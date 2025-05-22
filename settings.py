"""Модуль содержит настройки бота."""

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

REDIS_PERSISTENCE = {
    'HOST': os.getenv('REDIS_PERSISTENCE_HOST'),
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': None,
}
