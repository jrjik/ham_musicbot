"""Модуль содержит реализацию permission-класса."""

from typing import TYPE_CHECKING, Any

import music_bot.bot.screens
from music_bot.bot.client.redis_client import is_maintenance_mode
from hammett.core.permission import Permission

if TYPE_CHECKING:
    from typing import Self

    from telegram import Update
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


class MaintenancePermission(Permission):
    """Permission-класс для проверки режима обслуживания."""

    async def has_permission(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> bool:
        """Проверяет, выключен ли режим обслуживания."""
        return not await is_maintenance_mode()

    async def handle_permission_denied(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> bool | Any:
        """Обрабатывает отказ в доступе при включённом режиме обслуживания."""
        return await music_bot.bot.screens.maintenance_mode.MaintenanceScreen().jump(update, context)
