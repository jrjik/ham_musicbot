"""Модуль содержит реализацию карточки-исполнителя."""

import json
from typing import TYPE_CHECKING

from hammett.core import Button
from hammett.core.constants import RenderConfig
from hammett.core.handlers import register_button_handler

import screens

from backend.users.services import get_user_list, save_user_list
from screens.base import BaseScreen
from spotify import API_CLIENT

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class Artist(BaseScreen):
    """Экран карточки с информацией об артисте."""

    async def get_config(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> RenderConfig:
        """Метод отрисовки карточки исполнителя."""
        artist_data_raw = await self.get_payload(_update, _context)
        artist_name = json.loads(artist_data_raw).get('name')

        artist_info = API_CLIENT.get_artist_card_data(artist_name)
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
                [Button('🗑 Удалить исполнителя', source=self._delete_artist,
                        payload=json.dumps({'name': artist_name}))],
                *await self.add_artist_list_keyboard(_update, _context),
            ],
            cover=artist_info.get('image_url'),
        )

    @register_button_handler
    async def _delete_artist(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'State':
        """Метод для удаления артиста из списка."""
        user_id = update.effective_user.id
        artist_data = await self.get_payload(update, context)
        artist_name = json.loads(artist_data).get('name')

        current_list = await get_user_list(user_id)
        if artist_name in current_list:
            current_list.remove(artist_name)
            await save_user_list(user_id, current_list)

        return await screens.artist_list.ArtistList().move(update, context)
