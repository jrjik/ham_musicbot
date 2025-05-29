"""Модуль содержит реализацию экрана с редактированием списка артистов."""

from typing import TYPE_CHECKING

from hammett.core.constants import DEFAULT_STATE, RenderConfig
from hammett.core.handlers import register_typing_handler
from hammett.core.mixins import RouteMixin

from constants import INPUT_STATE
from database import save_user_list
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

ARTISTLIST_SCREEN_DESCRIPTION = (
    'Перечисли список любимых исполнителей через пробел'
    '\n'
    'Ниже ты можешь вернуться на начальный экран'
)

class ArtistListEdit(BaseScreen, RouteMixin):
    """Класс для редактирования списка исполнителей."""

    routes = (({DEFAULT_STATE}, INPUT_STATE),)

    description = ARTISTLIST_SCREEN_DESCRIPTION

    @register_typing_handler
    async def handle_text_(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'State':
        """Обработчик кнопки для записи списка исполнителей."""
        if update.message is None:
            return DEFAULT_STATE

        user_id = update.effective_user.id
        user_text = update.message.text
        items = [item.strip() for item in user_text.split(',')]
        save_user_list(user_id, items)

        await self.render(
            update,
            context,
            config=RenderConfig(
                as_new_message=True,
                description=(
                    f'Список сохранён в базу данных!\nВаш список: {', '.join(items)}'
                ),
                keyboard=[[self._get_back_button()]],
            ),
        )

        return DEFAULT_STATE
