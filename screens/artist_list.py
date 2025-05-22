"""Модуль содержит реализацию экрана со списком артистов."""
from typing import TYPE_CHECKING

from database import get_user_list
from screens.base import BaseScreen

if TYPE_CHECKING:
    from typing import Self

    from hammett.types import Keyboard
    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

class ArtistListShow(BaseScreen):
    """Класс для вывода списка исполнителей."""

    async def get_description(
        self: 'Self',
        update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> str:
        """Метод возвращает список исполнителей."""
        user_id = update.effective_user.id
        artists = get_user_list(user_id)

        if not artists:
            return '🎤 Ваш список исполнителей пуст'

        artists_list = '\n'.join(f'▫️ {artist}' for artist in artists)
        return f'🎤 Ваши исполнители:\n\n{artists_list}\n\nВсего: {len(artists)}'

    async def add_default_keyboard(
        self: 'Self',
        _update: 'Update | None',
        _context: 'CallbackContext[BT, UD, CD, BD]',
    ) -> 'Keyboard':
        """Метод добавляет кнопку возврата в главное меню на экран."""
        return [[self._get_back_button()]]
