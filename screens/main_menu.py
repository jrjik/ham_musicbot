"""Модуль содержит реализацию стартвого экрана с переходами."""

from typing import TYPE_CHECKING, Any

from hammett.conf import settings
from hammett.core import Button
from hammett.core.constants import RenderConfig, SourceTypes
from hammett.core.hider import ONLY_FOR_ADMIN, Hider
from hammett.core.mixins import StartMixin

from redis_client import is_maintenance_mode
from screens import admin_panel, artist_list, search_releases

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram import Update
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

    cover = settings.MEDIA_ROOT / 'image1.jpg'

    description = START_SCREEN_DESCRIPTION

    async def get_config(
        self: 'Self',
        update: 'Update',
        context: 'CallbackContext[BT, UD, CD, BD]',
        **kwargs: 'Any',
    ) -> RenderConfig:
        """Возвращает RenderConfig с учётом режима обслуживания."""
        user_id = update.effective_user.id

        if is_maintenance_mode() and user_id not in settings.ADMIN_GROUP:
            return RenderConfig(
                description=MAINTENANCE_SCREEN_DESCRIPTION,
                keyboard=[],
            )

        return await super().get_config(update, context, **kwargs)

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
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
                    search_releases.ArtistSearch,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    '⚙️ Режим обслуживания',
                    admin_panel.AdminPanel,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    hiders=Hider(ONLY_FOR_ADMIN),
                ),
            ],
        ]
