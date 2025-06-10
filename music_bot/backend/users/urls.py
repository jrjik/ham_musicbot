from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArtistListViewSet

router = DefaultRouter()
router.register(r'users', ArtistListViewSet, basename='userlist')

urlpatterns = [
    path('', include(router.urls)),
]
