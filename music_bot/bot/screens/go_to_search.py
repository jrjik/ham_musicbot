"""Модуль содержит базовые модули для экранов."""

from typing import TYPE_CHECKING

from hammett.conf import settings
from hammett.core import Button, Screen
from hammett.core.constants import SourceTypes

import screens
from screens import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class GoToSearch(BaseScreen):
    """В классе содержится кнопка возврата на StartScreen."""

    cover = settings.MEDIA_ROOT / 'default_cover.jpg'

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        return [
            [
                Button(
                    'К поиску',
                    screens.search_releases.ArtistSearchResult,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [self._get_main_menu_button()]
        ]
