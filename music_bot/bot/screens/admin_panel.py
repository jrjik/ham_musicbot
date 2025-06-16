"""Модуль содержит экран панели администратора, позволяющий переключать режим обслуживания."""

from typing import TYPE_CHECKING

import screens
from hammett.core import Button
from hammett.core.handlers import register_button_handler
from hammett.core.hider import ONLY_FOR_ADMIN, Hider
from redis_client import enable_maintenance
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import State, Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class AdminPanel(BaseScreen):
    """Экран панели администратора, доступный только админам."""

    description = (
        'Панель администратора\n\n'
        f'Текущий режим: Рабочий'
    )

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        return [
            [
                Button(
                    'Включить обслуживание',
                    source=self.enable,
                    hiders=Hider(ONLY_FOR_ADMIN),
                )
            ],
            [self._get_main_menu_button()],
        ]

    @register_button_handler
    async def enable(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]') \
        -> 'State':
        """Обработчик кнопки 'Включить обслуживание'.
        Включает режим обслуживания и возвращает пользователя на главный экран.
        """
        await enable_maintenance()
        return await screens.maintenance_mode.MaintenanceScreen().jump(update, context)
