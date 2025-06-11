from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import TelegramUserViewSet

router = DefaultRouter()
router.register(r'users', TelegramUserViewSet, basename='userlist')

urlpatterns = [
    path('', include(router.urls)),
]
