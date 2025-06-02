"""Модуль содержит настройки бота."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MEDIA_ROOT = Path(__file__).resolve().parent / 'media'

REDIS_PERSISTENCE = {
    'HOST': os.getenv('REDIS_PERSISTENCE_HOST'),
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': None,
}


SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')

SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
