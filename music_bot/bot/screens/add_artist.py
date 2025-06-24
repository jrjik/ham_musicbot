"""Модуль содержит реализацию экрана с редактированием списка артистов."""

from typing import TYPE_CHECKING

from music_bot.bot.client.backend_client import API_CLIENT
from music_bot.bot.constants import INPUT_STATE
from hammett.conf import settings
from hammett.core.constants import DEFAULT_STATE, RenderConfig
from hammett.core.handlers import register_typing_handler
from hammett.core.mixins import RouteMixin
from music_bot.bot.screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard, State
    from telegram import Update
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
    async def handle_text(
        self: 'Self',
        update: 'Update | None',
        context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'State':
        """Обработчик кнопки для записи исполнителей."""
        if (update is None or update.effective_user is None
            or update.message is None or update.message.text is None):
            return DEFAULT_STATE

        user_id = update.effective_user.id
        artist_name = update.message.text.strip()

        state = INPUT_STATE
        keyboard = []

        if len(artist_name) < settings.MIN_ARTIST_NAME_LENGTH or artist_name.isdigit():
            description = 'Исполнитель должен быть минимум из 3 символов и содержать буквы.'
        elif ',' in artist_name or '  ' in artist_name:
            description = 'Пожалуйста, введите только *одного* исполнителя.'
        else:
            existing_list = await API_CLIENT.get_user_list(user_id)
            updated_list = list({*existing_list, artist_name})
            await API_CLIENT.save_user_artists(user_id, updated_list)

            description = (
                f'✅ Исполнитель "{artist_name}" успешно добавлен.\n\n'
                f'🎤 Текущий список:\n' +
                '\n'.join(f'▫️ {artist}' for artist in updated_list)
            )
            keyboard = [[self._get_artist_list_button()]]
            state = DEFAULT_STATE

        await self.render(
            update,
            context,
            config=RenderConfig(
                as_new_message=True,
                description=description,
                keyboard=keyboard,
            ),
        )
        return state

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата в главное меню на экран."""
        return await self.add_artist_list_keyboard(_update, _context)
