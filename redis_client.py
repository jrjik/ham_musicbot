"""Модуль содержит функции для управления режимом обслуживания."""

import redis
from hammett.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_PERSISTENCE['HOST'],
    port=settings.REDIS_PERSISTENCE['PORT'],
    db=settings.REDIS_PERSISTENCE['DB'],
    password=settings.REDIS_PERSISTENCE.get('PASSWORD'),
    decode_responses=True,
)

MAINTENANCE_MODE_KEY = 'maintenance_mode'


def enable_maintenance() -> None:
    """Включает режим обслуживания, сохраняя значение в Redis."""
    redis_client.set(MAINTENANCE_MODE_KEY, 'on')


def disable_maintenance() -> None:
    """Выключает режим обслуживания, сохраняя значение в Redis."""
    redis_client.set(MAINTENANCE_MODE_KEY, 'off')


def is_maintenance_mode() -> bool:
    """Проверяет, включён ли режим обслуживания."""
    return redis_client.get(MAINTENANCE_MODE_KEY) == 'on'
