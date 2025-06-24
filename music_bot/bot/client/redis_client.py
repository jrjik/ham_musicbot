"""Модуль содержит функции для управления режимом обслуживания."""
from typing import Any

import redis.asyncio as redis
from hammett.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_PERSISTENCE['HOST'],
    port=settings.REDIS_PERSISTENCE['PORT'],
    db=settings.REDIS_INTERNAL_DB,
    password=settings.REDIS_PERSISTENCE.get('PASSWORD'),
)

MAINTENANCE_MODE_KEY = 'maintenance_mode'


async def enable_maintenance() -> None:
    """Включает режим обслуживания, сохраняя значение в Redis."""
    await redis_client.set(MAINTENANCE_MODE_KEY, 'on')


async def disable_maintenance() -> None:
    """Выключает режим обслуживания, сохраняя значение в Redis."""
    await redis_client.set(MAINTENANCE_MODE_KEY, 'off')


async def is_maintenance_mode() -> bool | Any:
    """Проверяет, включён ли режим обслуживания."""
    return await redis_client.get(MAINTENANCE_MODE_KEY) == 'on'
