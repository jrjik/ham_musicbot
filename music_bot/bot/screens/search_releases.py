"""Модуль содержит реализацию поиска релизов по списку исполнителей."""

import logging
from typing import TYPE_CHECKING

from client.backend_client import API_CLIENT
from client.spotify import SPOTIFY_API_CLIENT
from hammett.core.constants import RenderConfig
from screens.base import BaseScreen
from telegram import Update

if TYPE_CHECKING:
    from typing import Any, Self

    from telegram.ext import CallbackContext
    from telegram.ext._utils.types import BD, BT, CD, UD

logger = logging.getLogger(__name__)


class ArtistSearchResult(BaseScreen):
    """Класс поиска релизов."""

    async def get_config(
        self: 'Self',
        update: Update | None,
        _context: 'CallbackContext[BT, UD, CD, BD]',
        **_kwargs: 'Any',
    ) -> 'RenderConfig':
        """Метод класса возвращает релизы, которые потом передаются в экран."""
        if (update is None or update.effective_user is None
            or update.callback_query is None or update.update_id is None):
            return RenderConfig()

        user_id = update.effective_user.id
        artists = await API_CLIENT.get_user_list(user_id)

        if not artists:
            description = ('❌ У вас ещё нет списка исполнителей\n'
                           '\nПожалуйста, сначала создайте список через меню')
        elif update.callback_query and update.callback_query.data:
            results = SPOTIFY_API_CLIENT.fetch_last_friday_releases(artists)
            previous_friday = SPOTIFY_API_CLIENT.get_previous_friday()
            description = SPOTIFY_API_CLIENT.format_results(results, previous_friday)
        else:
            description = 'Нажмите кнопку для поиска релизов'

        return RenderConfig(description=description)



