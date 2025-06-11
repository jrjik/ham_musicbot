"""Модуль для запуска бота."""
import django
from constants import INPUT_STATE
from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE
from hammett.core.persistence import RedisPersistence
from screens import (
    AdminPanel,
    Artist,
    ArtistAdd,
    ArtistList,
    ArtistSearchResult,
    GoToSearch,
    MainMenu,
    MaintenanceScreen,
)

django.setup()

def main() -> None:
    """Запуск бота."""
    bot = Bot(
        'Ham_MusicBot',
        entry_point=MainMenu,
        persistence=RedisPersistence(),
        states={
            DEFAULT_STATE: {
                MainMenu,
                ArtistSearchResult,
                ArtistList,
                Artist,
                AdminPanel,
                MaintenanceScreen,
                GoToSearch,
            },
            INPUT_STATE: {ArtistAdd, MainMenu, ArtistList},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
