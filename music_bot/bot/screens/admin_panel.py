"""Модуль содержит экран панели администратора, позволяющий переключать режим обслуживания."""

from typing import TYPE_CHECKING

from hammett.core import Button
from hammett.core.constants import RenderConfig
from hammett.core.handlers import register_button_handler
from hammett.core.hider import ONLY_FOR_ADMIN, Hider

import screens
from redis_client import enable_maintenance, is_maintenance_mode
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class AdminPanel(BaseScreen):
    """Экран панели администратора, доступный только админам."""

    async def get_config(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any') -> 'RenderConfig':
        """Формирует конфигурацию экрана в зависимости от текущего режима работы бота."""
        return RenderConfig(
            description=(
                'Панель администратора\n\n'
                  f'Текущий режим: {"Обслуживание" if await is_maintenance_mode() else "Рабочий"}'
            ),
            keyboard=[
                [
                    Button(
                        'Включить обслуживание',
                        source=self.enable,
                        hiders=Hider(ONLY_FOR_ADMIN),
                    ),
                ],
                [self._get_main_menu_button()]
            ],
        )

    @register_button_handler
    async def enable(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]' ) \
        -> 'State':
        """Обработчик кнопки 'Включить обслуживание'.
        Включает режим обслуживания и возвращает пользователя на главный экран.
        """
        await enable_maintenance()
        return await screens.maintenance_mode.MaintenanceScreen().jump(update, context)
