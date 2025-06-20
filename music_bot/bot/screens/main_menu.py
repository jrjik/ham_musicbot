"""Модуль содержит реализацию стартвого экрана с переходами."""

from typing import TYPE_CHECKING

from hammett.conf import settings
from hammett.core import Button
from hammett.core.constants import SourceTypes
from hammett.core.hider import ONLY_FOR_ADMIN, Hider
from hammett.core.mixins import StartMixin
from screens import admin_panel, artist_list, go_to_search
from telegram import Update

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

START_SCREEN_DESCRIPTION = (
    '🎶 <b>HMusicBot</b>\n'
    '\n'
    'Храните список любимых артистов и получайте информацию о новых релизах:\n'
    '\n'
    '<i>Выберите действие в меню ниже</i>'
)

MAINTENANCE_SCREEN_DESCRIPTION = (
    '<b>Технические работы</b>\n\n'
)


class MainMenu(StartMixin):
    """Класс предоставляет стартовый экран с переходами на другие."""

    cover = settings.MEDIA_ROOT / 'default_cover.jpg'

    description = START_SCREEN_DESCRIPTION

    async def add_default_keyboard(
        self: 'Self',
        _update: Update | None,
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет клавиатуру с кнопками на экран."""
        return [
            [
                Button(
                    'Мои исполнители',
                    artist_list.ArtistList,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    'Поиск релизов',
                    go_to_search.GoToSearch,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    'Панель админа',
                    admin_panel.AdminPanel,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    hiders=Hider(ONLY_FOR_ADMIN),
                ),
            ],
        ]
