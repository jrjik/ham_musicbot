"""Модуль для запуска бота."""

from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE
from hammett.core.persistence import RedisPersistence

from constants import INPUT_STATE
from screens.artist_list import ArtistListShow
from screens.artist_list_edit import ArtistListEdit
from screens.search_releases import ArtistSearch
from screens.start_screen import StartScreen


def main() -> None:
    """Запуск бота."""
    bot = Bot(
        'Ham_MusicBot',
        entry_point=StartScreen,
        persistence=RedisPersistence(),
        states={
            DEFAULT_STATE: {StartScreen, ArtistListShow, ArtistSearch},
            INPUT_STATE: {ArtistListEdit, StartScreen},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
