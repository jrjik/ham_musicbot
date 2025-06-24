"""Корневой модуль пакета с экранами."""

from music_bot.bot.screens.add_artist import ArtistAdd
from music_bot.bot.screens.admin_panel import AdminPanel
from music_bot.bot.screens.artist import Artist
from music_bot.bot.screens.artist_list import ArtistList
from music_bot.bot.screens.base import BaseScreen
from music_bot.bot.screens.go_to_search import GoToSearch
from music_bot.bot.screens.main_menu import MainMenu
from music_bot.bot.screens.maintenance_mode import MaintenanceScreen
from music_bot.bot.screens.search_releases import ArtistSearchResult

__all__ = [
    'AdminPanel',
    'Artist',
    'ArtistAdd',
    'ArtistList',
    'ArtistSearchResult',
    'BaseScreen',
    'GoToSearch',
    'MainMenu',
    'MaintenanceScreen',
]
