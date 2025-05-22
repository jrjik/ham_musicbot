"""Модуль содержит реализацию стартвого экрана с переходами."""
from typing import TYPE_CHECKING

from hammett.core import Button
from hammett.core.constants import SourceTypes
from hammett.core.mixins import StartMixin

from screens.artist_list import ArtistListShow
from screens.artist_list_edit import ArtistListEdit
from screens.search_releases import ArtistSearch

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


class StartScreen(StartMixin):
    """Класс предоставляет стартовый экран с переходами на другие."""

    description = START_SCREEN_DESCRIPTION

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет клавиатуру с кнопками на экран."""
        return [
            [
                Button(
                    'Поиск релизов',
                    ArtistSearch,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    'Создать Список исполнителей',
                    ArtistListEdit,
                    source_type=SourceTypes.MOVE_ALONG_ROUTE_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    'Мой список',
                    ArtistListShow,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
        ]
