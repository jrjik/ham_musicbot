"""Модуль содержит клиент Spotify API для получения информации об артистах и релизах."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any, Self

import spotipy
from hammett.conf import settings
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)

FRIDAY_WEEKDAY = 4  # пятница (0-понедельник, 6-воскресенье)
MIDDAY_HOUR = 12


class SpotifyAPIClient:
    """Клиент для взаимодействия с API Spotify."""

    def __init__(self: Self) -> None:
        """Инициализация клиента."""
        self._sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET,
            ),
        )

    def get_previous_friday(self) -> str:
        """Возвращает дату прошлой пятницы в формате YYYY-MM-DD."""
        today = datetime.now(UTC)
        days_ago = (today.weekday() - FRIDAY_WEEKDAY) % 7
        if days_ago == 0 and today.hour < MIDDAY_HOUR:
            days_ago = 7
        previous_friday = today - timedelta(days=days_ago)
        return previous_friday.strftime('%Y-%m-%d')

    def get_artist_card_data(
        self,
        artist_name: str,
    ) -> dict[str, str | list[str] | int | None] | None:
        """Получить информацию об артисте из Spotify."""
        results = self._sp.search(q=artist_name, type='artist', limit=1)
        items = results.get('artists', {}).get('items', [])
        if not items:
            return None

        artist = items[0]
        return {
            'name': artist['name'],
            'genres': artist['genres'],
            'popularity': artist['popularity'],
            'url': artist['external_urls']['spotify'],
            'image_url': artist['images'][0]['url'] if artist['images'] else None,
        }

    def fetch_releases_by_date(
        self: Self,
        artists: list[str],
        target_date: str,
    ) -> dict[str, list[dict[str, Any]]]:
        """Получить релизы артистов по конкретной дате."""
        results = {}
        for artist in artists:
            try:
                query = f'artist:{artist}'
                releases = self._sp.search(
                    q=query,
                    type='album',
                    limit=settings.SEARCH_LIMIT,
                )

                matched_releases = [
                    album for album in releases['albums']['items']
                    if album.get('release_date') == target_date
                ]

                if matched_releases:
                    results[artist] = matched_releases
            except SpotifyException:
                logger.exception('Ошибка при поиске релизов для %s', artist)
                continue
        return results

    def fetch_last_friday_releases(
        self: Self,
        artists: list[str],
    ) -> dict[str, list[dict[str, Any]]]:
        """Получить релизы артистов за прошлую пятницу."""
        previous_friday = self.get_previous_friday()
        logger.info('Поиск релизов за %s', previous_friday)
        return self.fetch_releases_by_date(artists, previous_friday)

    def get_release_text_for_user(self: Self, artists: list[str]) -> str:
        """Вернуть текст с релизами для заданных артистов."""
        releases = self.fetch_last_friday_releases(artists)
        if not releases:
            return 'Ничего нового не найдено 💤'

        lines = []
        for artist, albums in releases.items():
            for album in albums:
                name = album.get('name')
                release_type = album.get('album_type', '').capitalize()
                url = album.get('external_urls', {}).get('spotify', '')
                lines.append(f'▫️ *{artist}* — {release_type}: [{name}]({url})')

        return '\n'.join(lines)

    def format_date_ru(self, date_str: str) -> str:
        """Преобразует дату из 'YYYY-MM-DD' в формат 'день/месяц'."""
        months = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря',
        ]
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=UTC)
            return f'{date.day} {months[date.month - 1]}'
        except ValueError:
            return date_str

    def format_results(
        self: 'Self',
        results: dict[str, list[dict[str, 'Any']]],
        release_date: str,
    ) -> str:
        """Форматирует результаты с указанием даты релиза."""
        if not results:
            return f'На {SPOTIFY_API_CLIENT.format_date_ru(release_date)} релизов не найдено.'

        message = f'🎵 Найденные релизы ({SPOTIFY_API_CLIENT.format_date_ru(release_date)}):\n\n'
        for artist, releases in results.items():
            message += f'🎤 {artist}:\n'
            for release in releases:
                message += f'▫️ {release["name"]} ({release["album_type"]})\n'
                message += f'   Ссылка: {release["external_urls"]["spotify"]}\n\n'
        return message

SPOTIFY_API_CLIENT = SpotifyAPIClient()
