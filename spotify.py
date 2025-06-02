"""SpotifyAPIClient"""

import logging

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

logger = logging.getLogger(__name__)

class SpotifyAPIClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        ))

    def get_artist_card_data(self, artist_name: str) -> dict | None:
        """Получить информацию об артисте из Spotify."""
        results = self.sp.search(q=artist_name, type='artist', limit=1)
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

    def fetch_releases_by_date(self, artists: list[str], target_date: str) -> dict[str, list[dict]]:
        """Получить релизы артистов по дате."""
        results = {}
        for artist in artists:
            try:
                query = f'artist:{artist} year:2023'
                releases = self.sp.search(q=query, type='album', limit=10)

                matched_releases = [
                    item for item in releases['albums']['items']
                    if item['release_date'] == target_date
                ]

                if matched_releases:
                    results[artist] = matched_releases
            except SpotifyException:
                logger.exception(f'Ошибка при получении релизов артиста {artist}')
        return results

API_CLIENT = SpotifyAPIClient()
