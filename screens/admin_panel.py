"""Модуль содержит экран панели администратора, позволяющий переключать режим обслуживания."""
from typing import TYPE_CHECKING

from hammett.conf import settings
from hammett.core import Button
from hammett.core.constants import RenderConfig
from hammett.core.handlers import register_button_handler
from hammett.core.hider import ONLY_FOR_ADMIN, Hider

import screens
from redis_client import disable_maintenance, enable_maintenance, is_maintenance_mode
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Any, Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class AdminPanel(BaseScreen):
    """Экран панели администратора, доступный только админам."""

    cover = settings.MEDIA_ROOT / 'image1.jpg'

    async def get_config(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any') -> 'RenderConfig':
        """Формирует конфигурацию экрана в зависимости от текущего режима работы бота."""
        return RenderConfig(
            description='Панель администратора\n\n'
                        f'Текущий режим: {"Обслуживание" if is_maintenance_mode() else "Рабочий"}',
            keyboard=[
                [Button(
                    'Включить обслуживание',
                    source=self.enable,
                    hiders=Hider(ONLY_FOR_ADMIN),

                ),
                ],
                [Button
                 ('Отключить обслуживание',
                  source=self.disable,
                  hiders=Hider(ONLY_FOR_ADMIN),
                  ),
                 ],
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
        enable_maintenance()
        return await screens.main_menu.MainMenu().move(update, context)

    @register_button_handler
    async def disable(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]')\
        -> 'State':
        """Обработчик кнопки 'Отключить обслуживание'.
        Выключает режим обслуживания и возвращает пользователя на главный экран.
        """
        disable_maintenance()
        return await screens.main_menu.MainMenu().move(update, context)
