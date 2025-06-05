"""Модуль для запуска бота."""
import os
import sys

import django

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE
from hammett.core.persistence import RedisPersistence

from constants import INPUT_STATE
from screens import AdminPanel, Artist, ArtistAdd, ArtistList, ArtistSearchResult, MainMenu, MaintenanceScreen, \
    GoToSearch


def main() -> None:
    """Запуск бота."""
    bot = Bot(
        'Ham_MusicBot',
        entry_point=MainMenu,
        persistence=RedisPersistence(),
        states={
            DEFAULT_STATE: {MainMenu, ArtistSearchResult, ArtistList, Artist, AdminPanel, MaintenanceScreen, GoToSearch},
            INPUT_STATE: {ArtistAdd, MainMenu, ArtistList},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
