"""Модуль содержит реализацию экрана обслуживания."""

from typing import TYPE_CHECKING

import screens
from client.redis_client import disable_maintenance
from hammett.conf import settings
from hammett.core import Button
from hammett.core.handlers import register_button_handler
from hammett.core.hider import ONLY_FOR_ADMIN, Hider
from hammett.core.permission import ignore_permissions
from permissions import MaintenancePermission
from screens import BaseScreen

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import Keyboard, State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class MaintenanceScreen(BaseScreen):
    """Экран, отображаемый в режиме обслуживания."""

    cover = settings.MEDIA_ROOT / 'maintenance_cover.jpg'

    description = 'Бот находится на техническом обслуживании.\nПопробуйте позже.'

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Добавляет клавиатуру с кнопками на экран."""
        return [
            [
                Button(
                    'Отключить обслуживание',
                    source=self.disable,
                    hiders=Hider(ONLY_FOR_ADMIN),
                ),
            ],
            [self._get_main_menu_button()],
        ]

    @ignore_permissions([MaintenancePermission])
    @register_button_handler
    async def disable(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]') \
        -> 'State':
        """Обработчик кнопки 'Отключить обслуживание'."""
        await disable_maintenance()
        return await screens.main_menu.MainMenu().move(update, context)

    @ignore_permissions([MaintenancePermission])
    async def jump(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
        **kwargs: 'Any',
    ) -> 'State':
        """Переход к экрану через jump, игнорируя проверку доступа."""
        return await super().jump(update, context, **kwargs)
