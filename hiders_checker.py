"""Модуль содержит кастомные Hider-проверки для управления доступом к кнопкам."""

from typing import TYPE_CHECKING

from hammett.conf import settings
from hammett.core.hider import HidersChecker
from telegram.ext import CallbackContext
from telegram.ext._utils.types import BD, BT, CD, UD

from redis_client import is_maintenance_mode

if TYPE_CHECKING:
    from typing import Self

    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD


ONLY_IF_NOT_IN_MAINTENANCE = 3

async def not_in_maintenance(
    _update: 'Update | None',
    _context: 'CallbackContext[BT, UD, CD, BD]') -> bool:
    """Проверка, что бот не находится в режиме обслуживания."""
    return not is_maintenance_mode()


class MyHidersChecker(HidersChecker):
    """Класс с кастомными правилами отображения кнопок."""

    async def is_admin(
        self: 'Self',
        update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]') -> bool:
        """Проверка, является ли пользователь администратором."""
        return update.effective_user.id in settings.ADMIN_GROUP

    custom_hiders = {
        ONLY_IF_NOT_IN_MAINTENANCE: not_in_maintenance,
    }
