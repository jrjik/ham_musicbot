"""Модуль содержит реализацию экрана с редактированием списка артистов."""

from typing import TYPE_CHECKING

from bot.backend_client import API_CLIENT
from constants import INPUT_STATE
from hammett.core.constants import DEFAULT_STATE, RenderConfig
from hammett.core.handlers import register_typing_handler
from hammett.core.mixins import RouteMixin
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard, State
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

ARTISTLIST_SCREEN_DESCRIPTION = (
    'Введите нового исполнителя'
    '\n'
)


class ArtistAdd(BaseScreen, RouteMixin):
    """Класс для редактирования списка исполнителей."""

    description = ARTISTLIST_SCREEN_DESCRIPTION

    routes = (({DEFAULT_STATE}, INPUT_STATE),)

    @register_typing_handler
    async def handle_text_(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'State':
        """Обработчик кнопки для записи исполнителей."""
        if update.message is None:
            return DEFAULT_STATE

        user_id = update.effective_user.id
        artist_name = update.message.text.strip()

        if ',' in artist_name or '  ' in artist_name:
            await self.render(
                update,
                context,
                config=RenderConfig(
                    as_new_message=True,
                    description='Пожалуйста, введите только *одного* исполнителя.',
                ),
            )
            return INPUT_STATE

        existing_list = await API_CLIENT.get_user_list(user_id)
        updated_list = list({*existing_list, artist_name})
        await API_CLIENT.save_user_artists(user_id, updated_list)

        await self.render(
            update,
            context,
            config=RenderConfig(
                as_new_message=True,
                description=(
                    f'✅ Исполнитель "{artist_name}" успешно добавлен.\n\n'
                    f'🎤 Текущий список:\n' +
                    '\n'.join(f'▫️ {artist}' for artist in updated_list)
                ),
                keyboard=[[self._get_artist_list_button()]],
            ),
        )
        return DEFAULT_STATE

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата в главное меню на экран."""
        return await self.add_artist_list_keyboard(_update, _context)
