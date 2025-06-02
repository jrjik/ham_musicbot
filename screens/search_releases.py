"""Модуль содержит реализацию поиска релизов по списку исполнителей."""

import logging
from typing import TYPE_CHECKING

import spotipy
from hammett.conf import settings
from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes
from hammett.core.handlers import register_button_handler
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from database import get_user_list
from screens.base import BaseScreen

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

        config = RenderConfig()

        if not artists:
            config.description = (
                '❌ У вас ещё нет списка исполнителей\n\n'
                'Пожалуйста, сначала создайте список через меню'
            )
        elif 'spotify_results' in context.user_data:
            config.description = self._format_results(context.user_data['spotify_results'])
        else:
            config.description = 'Нажмите кнопку для поиска релизов'

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
        config.keyboard = keyboard

        return config

    async def _fetch_spotify_data(
        self: 'Self',
        artists: 'list',
        target_date: 'str',
    ) -> dict:
        """Функция парсинга релизов по списку исполнителей."""
        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET

        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret,
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)

        results = {}
        for artist in artists:
            try:
                query = f'artist:{artist} year:2023'
                releases = sp.search(q=query, type='album', limit=10)

                matched_releases = [
                    item
                    for item in releases['albums']['items']
                    if item['release_date'] == target_date
                ]

                if matched_releases:
                    results[artist] = matched_releases
            except SpotifyException:
                logger.exception('Ошибка подключения к Spotify API')

        return results

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
        """Обработчик на кнопку для поиска релизов.
        После нажатия подгружает список из базы
        и передает в функцию для парсинга.
        """
        user_id = update.effective_user.id
        artists = get_user_list(user_id)
        results = await self._fetch_spotify_data(artists, '2023-11-10')
        context.user_data['spotify_results'] = results

        return await self.move(update, context)

class SpotifyArtistMixin:
    """Класс для поиска информации для карточки исполнителя."""

    async def _fetch_artist_info(self, artist_name: str) -> dict | None:
        """Метод для поиска информации об исполнителе."""
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        ))
        results = sp.search(q=artist_name, type='artist', limit=1)
        items = results.get('artists', {}).get('items')
        if not items:
            return None
        artist = items[0]
        return {
            'name': artist['name'],
            'genres': artist['genres'],
            'popularity': artist['popularity'],
            'url': artist['external_urls']['spotify'],
            'image_url': artist['images'][0]['url'] if artist.get('images') else None,
        }
