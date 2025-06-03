"""Модуль содержит настройки бота."""

import os
from pathlib import Path

from dotenv import load_dotenv


#
# Основные настройки бота
#

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
#
# Настройки бота (Hammett)
#

ADMIN_GROUP = []

HIDERS_CHECKER = 'hiders_checker.MyHidersChecker'  # Путь к классу проверки скрытых команд

#
# Настройки файловой системы
#
MEDIA_ROOT = Path(__file__).resolve().parent / 'media'  # Директория для медиафайлов

#
# Настройки Redis
#

REDIS_PERSISTENCE = {
    'HOST': os.getenv('REDIS_PERSISTENCE_HOST'),  # Хост Redis
    'PORT': 6379,                               # Порт Redis
    'DB': 0,                                    # Номер базы данных
    'PASSWORD': None,                           # Пароль (если требуется)
}

#
# Настройки Spotify API
#

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')      # ID клиента Spotify
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')  # Секретный ключ клиента Spotify