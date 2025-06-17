"""Модуль содержит клиент Django API для работы с таблицей users_userlist."""

import logging
from http import HTTPStatus
from typing import Self

import aiohttp
from hammett.conf import settings

logger = logging.getLogger(__name__)


class APIClient:
    """Клиент для взаимодействия с Django API."""

    def __init__(self: Self) -> None:
        """Инициализация клиента."""
        self._base_url = settings.API_BASE_URL

    async def get_user_list(self: Self, telegram_id: int) -> list[str]:
        """Получить список артистов пользователя по telegram_id."""
        url = f'{self._base_url}/users/{telegram_id}/'
        async with aiohttp.ClientSession() as session, \
            session.get(url) as resp:
            if resp.status == HTTPStatus.OK:
                data = await resp.json()
                return [item.strip() for item in data['items'] if item.strip()]
            if resp.status != HTTPStatus.NOT_FOUND:
                logger.error(
                    'Ошибка при получении пользователя %s: %s',
                    telegram_id,
                    resp.status,
                )
            return []

    async def save_user_artists(
        self: Self,
        telegram_id: int,
        artist_list: list[str],
    ) -> None:
        """Сохранить или обновить список артистов пользователя."""
        payload = {'telegram_id': telegram_id, 'items': sorted(set(artist_list))}
        url = f'{self._base_url}/users/{telegram_id}/'
        async with aiohttp.ClientSession() as session, \
            session.put(url, json=payload) as resp:
            if resp.status == HTTPStatus.NOT_FOUND:
                post_url = f'{self._base_url}/users/'
                async with session.post(post_url, json=payload) as post_resp:
                    if post_resp.status not in (HTTPStatus.OK, HTTPStatus.CREATED):
                        logger.error(
                            'Ошибка при создании пользователя %s: %s',
                            telegram_id,
                            post_resp.status,
                        )
            elif resp.status not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
                logger.error(
                    'Ошибка при обновлении пользователя %s: %s',
                    telegram_id,
                    resp.status,
                )


API_CLIENT = APIClient()
