from rest_framework import serializers

from .models import ArtistList


class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistList
        fields = '__all__'
