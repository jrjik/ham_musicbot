"""init.py."""

from screens.add_artist import ArtistAdd
from screens.admin_panel import AdminPanel
from screens.artist import Artist
from screens.artist_list import ArtistList
from screens.base import BaseScreen
from screens.go_to_search import GoToSearch
from screens.main_menu import MainMenu
from screens.maintenance_mode import MaintenanceScreen
from screens.search_releases import ArtistSearchResult

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
