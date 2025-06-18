"""Модуль содержит клиент Spotify API для получения информации об артистах и релизах."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Self

import spotipy
from hammett.conf import settings
from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
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
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
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

    def get_artist_card_data(self, artist_name: str) -> dict | None:
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
    ) -> dict[str, list[dict]]:
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

    def fetch_last_friday_releases(self: Self, artists: list[str]) -> dict[str, list[dict]]:
        """Получить релизы артистов за прошлую пятницу."""
        previous_friday = self.get_previous_friday()
        logger.info('Поиск релизов за %s', previous_friday)
        return self.fetch_releases_by_date(artists, previous_friday)


SPOTIFY_API_CLIENT = SpotifyAPIClient()
