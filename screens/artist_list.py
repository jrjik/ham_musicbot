"""Модуль содержит реализацию экрана."""

from typing import TYPE_CHECKING

from hammett.core import Button
from hammett.core.constants import SourceTypes

from database import get_user_list
from screens.artist_list_edit import ArtistListEdit
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class ArtistListSc(BaseScreen):
    """Класс содержит реализацию экрана с выводом текущего списка исполнителей
    и редактированием существующего.
    """

    async def get_description(
        self: 'Self',
        update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> str:
        """Метод возвращает список исполнителей."""
        user_id = update.effective_user.id
        artists = get_user_list(user_id)

        if not artists:
            return '🎤 Ваш список исполнителей пуст'

        artists_list = '\n'.join(f'▫️ {artist}' for artist in artists)
        return f'🎤 Ваши исполнители:\n\n{artists_list}\n\nВсего: {len(artists)}'

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет клавиатуру с кнопками на экран."""
        return [
            [
                Button(
                    'Добавить список',
                    ArtistListEdit,
                    source_type=SourceTypes.MOVE_ALONG_ROUTE_SOURCE_TYPE,
                ),
            ],
            [
                self._get_back_button(),
            ],
        ]
