"""Модуль содержит настройки бота."""

import os
from pathlib import Path

from dotenv import load_dotenv

#
# Настройки бота
#

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

ADMIN_GROUP = {int(os.getenv('ADMIN_GROUP'))}

PERMISSIONS = [
    'permissions.MaintenancePermission',
]

HIDERS_CHECKER = 'hiders_checker.MyHidersChecker'

MEDIA_ROOT = Path(__file__).resolve().parent / 'media'

REDIS_PERSISTENCE = {
    'HOST': os.getenv('REDIS_PERSISTENCE_HOST'),
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': None,
}

REDIS_INTERNAL_DB = 1
API_BASE_URL = 'http://127.0.0.1:8000/api/'
#
# Настройки Spotify API
#

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
