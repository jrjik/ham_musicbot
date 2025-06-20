"""Модуль содержит реализацию карточки-исполнителя."""

import json
from typing import TYPE_CHECKING


import screens
from client.backend_client import API_CLIENT
from client.spotify import SPOTIFY_API_CLIENT
from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes, DEFAULT_STATE
from hammett.core.handlers import register_button_handler
from screens.base import BaseScreen
from telegram import Update

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD
    from telegram import Update

class Artist(BaseScreen):
    """Экран карточки с информацией об артисте."""

    async def get_config(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> RenderConfig:
        """Метод отрисовки карточки исполнителя."""
        artist_data_raw = await self.get_payload(update, context)
        payload = json.loads(artist_data_raw)
        artist_name = payload.get('name')
        page = payload.get('page', 0)

        artist_info = SPOTIFY_API_CLIENT.get_artist_card_data(artist_name)
        if not artist_info:
            return RenderConfig(description='Не удалось найти информацию об артисте.')

        description = (
            f"🎤 *{artist_info['name']}*\n\n"
            f" Жанры: {', '.join(artist_info['genres']) or 'не указаны'}\n"
            f" Популярность: {artist_info['popularity']} / 100\n"
            f"🔗 [Слушать в Spotify]({artist_info['url']})"
        )

        return RenderConfig(
            description=description,
            keyboard=[
                [
                    Button(
                        '🗑 Удалить исполнителя',
                        source=self._delete_artist,
                        payload=json.dumps({'name': artist_name, 'page': page}),
                    ),
                ],
                [
                    Button(
                        '⬅️ Назад к списку',
                        screens.artist_list.ArtistList,
                        source_type=SourceTypes.MOVE_SOURCE_TYPE,
                        payload=json.dumps({'page': page}),
                    ),
                ],
            ],
            cover=artist_info.get('image_url'),
        )

    @register_button_handler
    async def _delete_artist(
        self: 'Self',
        update: Update | None,
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'State':
        """Метод для удаления артиста из списка."""
        if update is None or update.effective_user is None or update.update_id is None:
            return DEFAULT_STATE

        user_id = update.effective_user.id
        artist_data = await self.get_payload(update, context)
        payload = json.loads(artist_data)
        artist_name = payload.get('name')
        page = payload.get('page', 0)

        current_list = await API_CLIENT.get_user_list(user_id)
        if artist_name in current_list:
            current_list.remove(artist_name)
            await API_CLIENT.save_user_artists(user_id, current_list)

        return await screens.artist_list.ArtistList().move(update, context, payload=json.dumps({'page': page}))
