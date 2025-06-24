from rest_framework import viewsets

from users.models import TelegramUser
from users.serializers import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'telegram_id'
