"""Модуль для запуска бота."""

from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE
from hammett.core.persistence import RedisPersistence

from constants import INPUT_STATE
from screens import Artist, ArtistAdd, ArtistList, ArtistSearch, MainMenu


def main() -> None:
    """Запуск бота."""
    bot = Bot(
        'Ham_MusicBot',
        entry_point=MainMenu,
        persistence=RedisPersistence(),
        states={
            DEFAULT_STATE: {MainMenu, ArtistSearch, ArtistList, Artist},
            INPUT_STATE: {ArtistAdd, MainMenu, ArtistList},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
