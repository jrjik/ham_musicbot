"""Модуль для запуска бота."""
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
from screens.notification import send_friday_releases_notification


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
        job_configs=[
            {
                'callback': send_friday_releases_notification,
                'job_kwargs': {
                    'trigger': 'cron',
                    'day_of_week': 'fri',
                    'hour': 0,
                    'minute': 5,
                },
            },
            {
                'callback': send_friday_releases_notification,
                'job_kwargs': {
                    'trigger': 'interval',
                    'seconds': 15,
                },
            },
        ],
    )
    bot.run()


if __name__ == '__main__':
    main()
