"""Модуль содержит реализацию базы данных."""

import logging
import sqlite3
from sqlite3 import Connection, Error

logger = logging.getLogger(__name__)


def create_connection() -> Connection:
    """Функция подключения к базе."""
    conn = None
    try:
        return sqlite3.connect('user_lists.db')
    except Error:
        logger.exception('Ошибка подключения')
    return conn

def get_user_list(user_id: int) -> list[str]:
    """Функция запроса списка исполнителей из базы."""
    conn = create_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT items FROM user_lists WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            return [item.strip() for item in result[0].split(',')]
        return []

    except Error:
        logger.exception('Ошибка при чтении')
        return []
    finally:
        conn.close()

def init_db() -> None:
    """Функция инициализации базы и создание таблицы."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_lists (
                user_id INTEGER PRIMARY KEY,
                items TEXT
            )
        """)
            conn.commit()
        except Error:
            logger.exception('Ошибка при создании таблицы')
        finally:
            conn.close()


def save_user_list(user_id: int, items: list) -> None:
    """Функция сохранения списка исполнителей в базу."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            items_str = ', '.join(items)
            cursor.execute(
                'REPLACE INTO user_lists (user_id, items) VALUES (?, ?)',
                (user_id, items_str),
            )
            conn.commit()
            logger.info('Список для user_id = %s сохранён', user_id)
        except Error as e:
            logger.info('Ошибка при сохранении: %s', e)
        finally:
            conn.close()

init_db()
