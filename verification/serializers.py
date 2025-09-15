from rest_framework import serializers

from places.models import Candidate, PhotoURL, Submission
from . import models
from .models import Verification

class PhotoURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoURL
        fields = ['id', 'url']

class VerificationSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(source="candidate.id")
    # user_id = ModelField(model_field=User)

    class Meta:
        model = models.Verification
        fields = ('candidate', 'action', 'notes', 'by_user', 'created_at', 'last_modified_at')
        read_only_fields = ("id", "public_id", "created_at")


class VerificationActionSerializer(serializers.Serializer):
    candidate_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=[x.value for x in Verification.Actions])
    notes = serializers.CharField(required=False, allow_blank=True)
    merge_into_spot_id = serializers.IntegerField(required=False)


class CandidateQueueSerializer(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=Submission.Kind.choices, default=Submission.Kind.MANUAL)
    photo_urls = PhotoURLSerializer(many=True, read_only=True)

    class Meta:
        model  = Candidate
        fields = ("id","name","city", "state", "country", "score","source_kind","evidence", "photo_urls",
                  "price_band", "tags", "phone", "kind", "email", "website", "signals","lat","lng","raw_address")
