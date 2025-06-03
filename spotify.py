"""Модуль содержит клиент Spotify API для получения информации об артистах и релизах."""

import logging
from typing import Self

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

logger = logging.getLogger(__name__)

class SpotifyAPIClient:
    """Клиент для взаимодействия с API Spotify."""

    def __init__(self: 'Self') -> None:
        """Инициализация клиента."""
        self._sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        ))

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
        self: 'Self',
        artists: list[str],
        target_date: str,
    ) -> dict[str, list[dict]]:
        """Получить релизы артистов по дате."""
        results = {}
        for artist in artists:
            try:
                query = f'artist:{artist} year:2023'
                releases = self._sp.search(q=query, type='album', limit=10)

                matched_releases = [
                    item for item in releases['albums']['items']
                    if item['release_date'] == target_date
                ]

                if matched_releases:
                    results[artist] = matched_releases
            except SpotifyException:
                logger.exception('Ошибка при получении релизов артиста %s', artist)
        return results

API_CLIENT = SpotifyAPIClient()
