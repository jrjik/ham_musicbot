"""Модуль содержит реализацию поиска релизов по списку исполнителей."""

import logging
from typing import TYPE_CHECKING

from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes
from hammett.core.handlers import register_button_handler

from database import get_user_list
from screens.base import BaseScreen
from spotify import API_CLIENT

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

logger = logging.getLogger(__name__)


class ArtistSearch(BaseScreen):
    """Класс для поиска релизов по любимым исполнителям пользователя."""

    async def get_config(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> 'RenderConfig':
        """Собирает и возвращает конфигурацию для отображения экрана поиска релизов."""
        user_id = update.effective_user.id
        artists = get_user_list(user_id)

        if not artists:
            description = (
                '❌ У вас ещё нет списка исполнителей\n\n'
                'Пожалуйста, сначала создайте список через меню'
            )
        elif 'spotify_results' in context.user_data:
            description = self._format_results(context.user_data['spotify_results'])
        else:
            description = 'Нажмите кнопку для поиска релизов'

        keyboard = []
        if artists:
            keyboard.append([
                Button(
                    '🔍 Найти релизы',
                    source=self.search_releases_handler,
                    source_type=SourceTypes.HANDLER_SOURCE_TYPE,
                ),
            ])

        keyboard.append([self._get_main_menu_button()])

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
        user_id = update.effective_user.id
        artists = get_user_list(user_id)
        results = API_CLIENT.fetch_releases_by_date(artists, '2023-11-10')
        context.user_data['spotify_results'] = results

        return await self.move(update, context)

