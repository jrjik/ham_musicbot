"""Модуль содержит базовые модули для экранов."""

from typing import TYPE_CHECKING

from hammett.conf import settings
from hammett.core import Button, Screen
from hammett.core.constants import SourceTypes

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

import screens


class BaseScreen(Screen):
    """В классе содержится кнопка возврата на StartScreen."""

    cover = settings.MEDIA_ROOT / 'image1.jpg'

    @staticmethod
    def _get_main_menu_button() -> 'Button':

        return Button(
            '⬅️ В главное меню',
            source=screens.main_menu.MainMenu,
            source_type=SourceTypes.MOVE_SOURCE_TYPE,
        )

    @staticmethod
    def _get_artist_list_button() -> 'Button':
        return Button(
            '⬅️ Назад',
            source=screens.artist_list.ArtistList,
            source_type=SourceTypes.MOVE_SOURCE_TYPE,
        )

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата в главное меню на экран."""
        return [[self._get_main_menu_button()]]


    async def add_artist_list_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата назад."""
        return [[self._get_artist_list_button()]]
