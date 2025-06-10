"""Модуль содержит реализацию поиска релизов по списку исполнителей."""

import logging
from typing import TYPE_CHECKING

from backend_client import API_CLIENT
from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes
from hammett.core.handlers import register_button_handler
from screens.base import BaseScreen
from spotify import SPOTIFY_API_CLIENT

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

logger = logging.getLogger(__name__)


class ArtistSearchResult(BaseScreen):
    """Класс для поиска релизов по любимым исполнителям пользователя."""

    async def get_config(
        self: 'Self',
        update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> 'RenderConfig':
        """Собирает и возвращает конфигурацию для отображения экрана поиска релизов."""
        user_id = update.effective_user.id
        artists = await API_CLIENT.get_user_list(user_id)

        if not artists:
            description = (
                '❌ У вас ещё нет списка исполнителей\n\n'
                'Пожалуйста, сначала создайте список через меню'
            )
            keyboard = [[self._get_main_menu_button()]]
        else:
            if update.callback_query and update.callback_query.data:
                results = SPOTIFY_API_CLIENT.fetch_releases_by_date(artists, '2023-11-10')
                description = self._format_results(results)
            else:
                description = 'Нажмите кнопку для поиска релизов'

            keyboard = [[
                Button(
                    '🔍 Найти релизы',
                    source=self.search_releases_handler,
                    source_type=SourceTypes.HANDLER_SOURCE_TYPE,
                ),
            ],
                [self._get_main_menu_button()]]

        return RenderConfig(
            description=description,
            keyboard=keyboard,
        )

    def _format_results(
        self: 'Self',
        results: dict[str],
    )-> str:
        """Функция для форматирования спарщенных данных."""
        if not results:
            return 'На указанную дату релизов не найдено'

        message = '🎵 Найденные релизы (2023-11-10):\n\n'
        for artist, releases in results.items():
            message += f'🎤 {artist}:\n'
            for release in releases:
                message += f'▫️ {release['name']} ({release['album_type']})\n'
                message += f'   Ссылка: {release['external_urls']['spotify']}\n\n'

        return message

    @register_button_handler
    async def search_releases_handler(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'State':
        """Обработчик на кнопку для поиска релизов. После нажатия подгружает список из базы
        и передает в функцию для парсинга.
        """
        return await self.move(update, context)

