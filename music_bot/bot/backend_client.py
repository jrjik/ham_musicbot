"""Модуль содержит клиент Django API для работы с таблицей users_userlist."""

import logging
from typing import Self

import aiohttp
from hammett.conf import settings

logger = logging.getLogger(__name__)

# Константы для HTTP статусов
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_NOT_FOUND = 404


class DjangoAPIClient:
    """Клиент для взаимодействия с Django API."""

    def __init__(self: Self) -> None:
        """Инициализация клиента."""
        self._base_url = f"{settings.API_BASE_URL.rstrip('/')}/users/"

    async def get_user_list(self: Self, telegram_id: int) -> list[str]:
        """Получить список артистов пользователя по telegram_id."""
        url = f'{self._base_url}{telegram_id}/'
        async with aiohttp.ClientSession() as session, \
                session.get(url) as resp:
            if resp.status == HTTP_STATUS_OK:
                data = await resp.json()
                return [item.strip() for item in data['items'] if item.strip()]
            if resp.status != HTTP_STATUS_NOT_FOUND:
                logger.error(
                    'Ошибка при получении пользователя %s: %s',
                    telegram_id,
                    resp.status,
                )
            return []

    async def save_user_list(
        self: Self,
        telegram_id: int,
        artist_list: list[str],
    ) -> None:
        """Сохранить или обновить список артистов пользователя."""
        items_string = ','.join(sorted(set(artist_list)))
        payload = {'telegram_id': telegram_id, 'items': items_string}
        url = f'{self._base_url}{telegram_id}/'

        async with aiohttp.ClientSession() as session, \
                session.put(url, json=payload) as resp:
            if resp.status == HTTP_STATUS_NOT_FOUND:
                async with session.post(self._base_url, json=payload) as post_resp:
                    if post_resp.status not in (HTTP_STATUS_OK, HTTP_STATUS_CREATED):
                        logger.error(
                            'Ошибка при создании пользователя %s: %s',
                            telegram_id,
                            post_resp.status,
                        )
            elif resp.status not in (HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT):
                logger.error(
                    'Ошибка при обновлении пользователя %s: %s',
                    telegram_id,
                    resp.status,
                )


API_CLIENT = DjangoAPIClient()
