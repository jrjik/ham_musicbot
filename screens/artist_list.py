"""Модуль содержит реализацию экрана."""

import json
from typing import TYPE_CHECKING, Any

from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes

from database import get_user_list
from screens.add_artist import ArtistAdd
from screens.artist import Artist
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class ArtistList(BaseScreen):
    """Класс содержит реализацию экрана с выводом текущего списка исполнителей
    и редактированием существующего.
    """

    async def get_config(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> RenderConfig:
        """Метод для динамической отрисовки кнопок-исполнителей."""
        user_id = _update.effective_user.id
        artists = get_user_list(user_id)

        config = RenderConfig(
            description='🎤 Ваш список исполнителей:',
        )

        artist_buttons = [
            [
                Button(
                    artist,
                    Artist,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    payload=json.dumps({'name': artist}),
            ),
        ]
            for artist in artists
        ]

        config.keyboard = [
            *artist_buttons,
            [
                Button(
                    '➕ Добавить исполнителя',
                    ArtistAdd,
                    source_type=SourceTypes.MOVE_ALONG_ROUTE_SOURCE_TYPE,
            ),
            ],
                [self._get_main_menu_button()],
        ]

        return config
