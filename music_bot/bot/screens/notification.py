"""Модуль содержит реализацию уведомления, отправляемого по расписанию."""

import logging
from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponseError
from music_bot.bot.client.backend_client import API_CLIENT
from music_bot.bot.client.spotify import SPOTIFY_API_CLIENT
from hammett.core.constants import RenderConfig
from hammett.core.screen import DEFAULT_STATE
from hammett.types import State
from music_bot.bot.screens import BaseScreen

if TYPE_CHECKING:
    from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


class FridayNotification(BaseScreen):
    """Экран для отправки уведомлений о релизах."""


async def send_friday_releases_notification(context: 'CallbackContext[Any, Any, Any, Any]') -> State:
    """Задача для отправки уведомлений каждую пятницу."""
    user_ids = await API_CLIENT.get_all_user_ids()
    if not user_ids:
        return DEFAULT_STATE

    for user_id in user_ids:
        try:
            artists = await API_CLIENT.get_user_list(user_id)
            if not artists:
                continue

            releases = SPOTIFY_API_CLIENT.fetch_last_friday_releases(artists)
            previous_friday = SPOTIFY_API_CLIENT.get_previous_friday()
            description = SPOTIFY_API_CLIENT.format_results(releases, previous_friday)

            await FridayNotification().send(
                context,
                config=RenderConfig(
                    chat_id=user_id,
                    description=description,
                ),
            )
        except ClientResponseError as e:
            logger.info('Ошибка при отправке уведомления пользователю %s: %s',
                        user_id, e)
    return DEFAULT_STATE

