"""Модуль содержит реализацию экрана со списком исполнителей."""

import json
import math
from typing import TYPE_CHECKING
from typing import Any
from hammett.core.exceptions import PayloadIsEmpty

from client.backend_client import API_CLIENT
from hammett.conf import settings
from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes
from screens.add_artist import ArtistAdd
from screens.artist import Artist
from screens.base import BaseScreen
from telegram import Update

if TYPE_CHECKING:
    from typing import Any, Self

    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD
    from telegram import Update


def paginate(items: list[Any], page: int, page_size: int = settings.PAGE_SIZE) -> list[Any]:
    """Функция пагинации списка по 5 элементов/страницу."""
    start = page * page_size
    return items[start:start + page_size]


class ArtistList(BaseScreen):
    """Экран со списком артистов с циклической пагинацией."""

    async def get_config(
        self: 'Self',
        update: Update | None,
        context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> RenderConfig:
        """Метод отрисовки описания, кнопок-исполнителей и кнопок перехода."""
        if update is None or update.effective_user is None or update.update_id is None:
            return RenderConfig()

        user_id = update.effective_user.id
        artists = await API_CLIENT.get_user_list(user_id)

        total_pages = max(1, math.ceil(len(artists) / settings.PAGE_SIZE))

        page = 0
        if update.callback_query and update.callback_query.data:
            try:
                payload = json.loads(await self.get_payload(update, context))
                page = int(payload.get('page', 0))
            except (json.JSONDecodeError, ValueError, PayloadIsEmpty):
                page = 0

        page %= total_pages

        description = f'🎤 Ваш список исполнителей (страница {page + 1} из {total_pages}):'
        artists_on_page = paginate(artists, page)

        artist_buttons = [
            [
                Button(
                    artist,
                    Artist,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    payload=json.dumps({'name': artist, 'page': page}),
                ),
            ]
            for artist in artists_on_page
        ]

        nav_buttons = []
        if total_pages > 1:
            prev_page = (page - 1) % total_pages
            next_page = (page + 1) % total_pages
            nav_buttons = [
                Button(
                    '⬅️',
                    ArtistList,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    payload=json.dumps({'page': prev_page}),
                ),
                Button(
                    '➡️',
                    ArtistList,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    payload=json.dumps({'page': next_page}),
                ),
            ]

        keyboard = [*artist_buttons]
        if nav_buttons:
            keyboard.append(nav_buttons)

        keyboard.append([
            Button(
                '➕ Добавить исполнителя',
                ArtistAdd,
                source_type=SourceTypes.MOVE_ALONG_ROUTE_SOURCE_TYPE,
            ),
        ])
        keyboard.append([self._get_main_menu_button()])

        return RenderConfig(
            description=description,
            keyboard=keyboard,
        )
