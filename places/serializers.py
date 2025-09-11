from rest_framework import serializers

from . import models

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Spot
        fields = ('name', 'address', 'city', 'state', 'lat', 'lng')

class GetSpotSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Spot
        fields = (
            'name', 'address', 'city', 'state', 'lat', 'lng', 'country',
            'zipcode', 'price_band', 'tags', 'photos', 'open_hours', 'source'
        )