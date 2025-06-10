from rest_framework import viewsets

from .models import ArtistList
from .serializers import ArtistListSerializer


class ArtistListViewSet(viewsets.ModelViewSet):
    queryset = ArtistList.objects.all()
    serializer_class = ArtistListSerializer
    lookup_field = 'telegram_id'
