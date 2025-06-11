"""Модуль содержит кастомные Hider-проверки для управления доступом к кнопкам."""

from typing import TYPE_CHECKING

from hammett.conf import settings
from hammett.core.hider import HidersChecker
from telegram.ext import CallbackContext
from telegram.ext._utils.types import BD, BT, CD, UD

if TYPE_CHECKING:
    from typing import Self

    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

class MyHidersChecker(HidersChecker):
    """Класс с кастомными правилами отображения кнопок."""

    async def is_admin(
        self: 'Self',
        update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]') -> bool:
        """Проверка, является ли пользователь администратором."""
        return update.effective_user.id in settings.ADMIN_GROUP

