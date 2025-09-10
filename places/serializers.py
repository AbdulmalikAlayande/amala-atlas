from rest_framework import serializers
from rest_framework.fields import CharField, DecimalField, FloatField, JSONField, URLField, ModelField

from . import models


class CandidateSerializer(serializers.ModelSerializer):
    name = CharField(max_length=200)
    raw_address = CharField(max_length=300)
    lat = FloatField(allow_null=True)
    lng = FloatField(allow_null=True)
    city = CharField(max_length=120)
    country = CharField(max_length=120, default="Nigeria")
    source_url = URLField(max_length=500)
    source_kind = CharField(max_length=40)

    class Meta:
        models = models.Candidate
        fields = (
            'name', 'raw_address', 'lat', 'lng', 'city', 'country',
            'source_url', 'source_kind'
        )


class SubmitCandidateSerializer(serializers.Serializer):
    name        = serializers.CharField(max_length=200)
    address     = serializers.CharField(allow_blank=True, required=False)
    city        = serializers.CharField(required=False, allow_blank=True)
    lat         = serializers.FloatField(required=False)
    lng         = serializers.FloatField(required=False)
    price_band  = serializers.ChoiceField(choices=["₦","₦₦","₦₦₦"], required=False)
    photo_url   = serializers.URLField(required=False, allow_blank=True)
    submitted_by_email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs.get("address") and not attrs.get("city") and not (
            attrs.get("lat") is not None and attrs.get("lng") is not None
        ):
            raise serializers.ValidationError("Provide address or city or lat+lng.")
        return attrs


class CandidateOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Candidate
        fields = ("id","name","city","country","lat","lng","status","score","evidence","signals","created_at")


class SpotSerializer(serializers.ModelSerializer):
    name = CharField(max_length=200)
    lat = FloatField(allow_null=True)
    lng = FloatField(allow_null=True)
    address = CharField(max_length=120)
    city = CharField(max_length=120)
    state = CharField(max_length=120)
    country = CharField(max_length=120, default="Nigeria")
    zipcode = CharField(max_length=8)
    price_band = CharField(max_length=8)
    tags = JSONField(default=list)
    photos = JSONField(default=list)
    open_hours = JSONField(allow_null=True)
    source = CharField(max_length=20, default="verified")

    class Meta:
        models = models.Spot
        fields = (
            'name', 'address', 'city', 'state', 'country', 'zipcode', 'lat',
            'lng', 'price_band', 'tags', 'photos', 'open_hours', 'source'
        )


class VerificationSerializer(serializers.ModelSerializer):
    candidate = ModelField(model_field=models.Candidate)
    action = CharField(max_length=10)
    notes = CharField(max_length=200)
    # by_user = ModelField(model_field=User)

    class Meta:
        models = models.Verification
        fields = ('candidate', 'action', 'notes')
