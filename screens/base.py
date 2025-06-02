"""Модуль содержит базовые модули для экранов."""

from typing import TYPE_CHECKING

from hammett.core import Button, Screen
from hammett.core.constants import SourceTypes

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class BaseScreen(Screen):
    """В классе содержится кнопка возврата на StartScreen."""

    @staticmethod
    def _get_main_menu_button() -> 'Button':
        from screens.main_menu import StartScreen

        return Button(
            '⬅️ В главное меню',
            source=StartScreen,
            source_type=SourceTypes.MOVE_SOURCE_TYPE,
        )

    @staticmethod
    def _get_back_button() -> 'Button':
        from screens.artist_list import ArtistList

        return Button(
            '⬅️ Назад',
            source=ArtistList,
            source_type=SourceTypes.MOVE_SOURCE_TYPE,
        )

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата в главное меню на экран."""
        return [[self._get_main_menu_button()]]


    async def add_back_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата назад."""
        return [[self._get_back_button()]]
