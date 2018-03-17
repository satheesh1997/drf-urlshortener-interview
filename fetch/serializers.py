from rest_framework import serializers
from .models import Shorturl

class Shorturlserializer(serializers.Serializer):
    long_url  = serializers.URLField()
    short_url = serializers.CharField(max_length=8)

    def create(self, validated_data):
        return Shorturl.objects.create(**validated_data)