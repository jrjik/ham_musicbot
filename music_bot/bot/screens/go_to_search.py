"""Модуль содержит базовые модули для экранов."""

from typing import TYPE_CHECKING

import screens
from client.backend_client import API_CLIENT
from hammett.core import Button
from hammett.core.constants import SourceTypes
from screens import BaseScreen
from telegram import Update

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD
    from telegram import Update


class GoToSearch(BaseScreen):
    """В классе содержится кнопка возврата на StartScreen."""

    async def get_description(
        self: 'Self',
        update: Update | None,
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> str:
        """Метод для передачи в сообщение описания текущего списка исполнителя,
        по которому будет парсинг.
        """
        if update is None or update.effective_user is None or update.update_id is None:
            return ''

        user_id = update.effective_user.id
        artist_list = await API_CLIENT.get_user_list(user_id)

        if not artist_list:
            return ('У вас пока нет добавленных исполнителей. '
                    'Добавьте их, чтобы начать поиск релизов.')

        artist_lines = '\n\n'.join(artist_list)
        return (
            '🔎 Нажав на кнопку «К поиску», вы можете найти релизы для следующих исполнителей:\n\n'
            f'{artist_lines}'
        )

    async def add_default_keyboard(
        self: 'Self',
        _update: Update | None,
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Добавляет клавиатуру с кнопками на экран."""
        return [
            [
                Button(
                    'К поиску',
                    screens.search_releases.ArtistSearchResult,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [self._get_main_menu_button()],
        ]
