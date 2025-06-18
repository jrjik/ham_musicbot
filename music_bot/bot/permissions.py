"""Модуль содержит реализацию permission-класса."""

from typing import TYPE_CHECKING

import screens
from client.redis_client import is_maintenance_mode
from hammett.core.permission import Permission

if TYPE_CHECKING:
    from typing import Self

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
    ) -> bool:
        """Обрабатывает отказ в доступе при включённом режиме обслуживания."""
        return await screens.maintenance_mode.MaintenanceScreen().jump(update, context)
