from django.db import models

from commons.models import BaseModel
from users.models import User

"""
Amala Spot
"""
class Spot(BaseModel):
    name        = models.CharField(max_length=200)
    lat         = models.FloatField()
    lng         = models.FloatField()
    address     = models.TextField(blank=True)
    city        = models.CharField(max_length=120, blank=True)
    state       = models.CharField(max_length=120, blank=True)
    country     = models.CharField(max_length=120, default="Nigeria")
    zipcode     = models.CharField(max_length=8, blank=True)
    price_band  = models.CharField(max_length=8, blank=True)  # ₦ / ₦₦ / ₦₦₦
    tags        = models.JSONField(default=list, blank=True)
    photos      = models.JSONField(default=list, blank=True)  # [{url, by?, at}]
    open_hours  = models.JSONField(null=True, blank=True)
    source      = models.CharField(max_length=20, default="verified")

    class Meta:
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["lat","lng"]),
        ]


"""
Prospective Amala Spot
"""
class Candidate(BaseModel):
    name         = models.CharField(max_length=200)
    raw_address  = models.TextField(blank=True)
    lat          = models.FloatField(null=True, blank=True)
    lng          = models.FloatField(null=True, blank=True)
    city         = models.CharField(max_length=120, blank=True)
    country      = models.CharField(max_length=120, default="Nigeria")
    source_url   = models.URLField(max_length=500, blank=True)
    source_kind  = models.CharField(max_length=40, blank=True)  # blog|directory|social|user|agent
    price_band = models.CharField(max_length=8, blank=True)
    photo_url    = models.URLField(blank=True)
    open_hours  = models.JSONField(null=True, blank=True)
    submitted_by_email = models.EmailField(blank=True)
    evidence     = models.JSONField(default=list, blank=True)
    signals      = models.JSONField(default=dict, blank=True)
    score        = models.DecimalField(max_digits=4, decimal_places=3, default=0)  # 0.000..1.000
    dedupe_key   = models.CharField(max_length=128, blank=True)
    geo_precision= models.CharField(max_length=20, blank=True)  # address|poi|city
    status       = models.CharField(max_length=30, default="pending_verification")

    class Meta:
        indexes = [
            models.Index(fields=["status","-score"]),
            models.Index(fields=["dedupe_key"]),
        ]
        ordering = ["-score"]


"""
Submission (To Preserve raw user/agent form separate from Candidate
"""
class Submission(BaseModel):
    payload = models.JSONField(blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)