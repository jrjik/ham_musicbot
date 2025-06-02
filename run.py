"""Модуль для запуска бота."""

from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE
from hammett.core.persistence import RedisPersistence

from constants import INPUT_STATE
from screens.add_artist import ArtistAdd
from screens.artist import Artist
from screens.artist_list import ArtistList
from screens.main_menu import StartScreen
from screens.search_releases import ArtistSearch


def main() -> None:
    """Запуск бота."""
    bot = Bot(
        'Ham_MusicBot',
        entry_point=StartScreen,
        persistence=RedisPersistence(),
        states={
            DEFAULT_STATE: {StartScreen, ArtistSearch, ArtistList, Artist},
            INPUT_STATE: {ArtistAdd, StartScreen, ArtistList},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
