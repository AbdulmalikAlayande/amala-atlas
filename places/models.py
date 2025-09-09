from django.db import models

from commons.models import BaseModel
from users.models import User
from django.utils.translation import gettext_lazy as _


# Amala Spot
class Spot(BaseModel):
    name        = models.CharField(max_length=200)
    lat         = models.FloatField()
    lng         = models.FloatField()
    address     = models.TextField(blank=True)
    city        = models.CharField(max_length=120, blank=True)
    country     = models.CharField(max_length=120, default="Nigeria")
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


# Prospective Amala Spot
class Candidate(BaseModel):
    name         = models.CharField(max_length=200)
    raw_address  = models.TextField(blank=True)
    lat          = models.FloatField(null=True, blank=True)
    lng          = models.FloatField(null=True, blank=True)
    city         = models.CharField(max_length=120, blank=True)
    country      = models.CharField(max_length=120, default="Nigeria")
    source_url   = models.URLField(max_length=500, blank=True)
    source_kind  = models.CharField(max_length=40, blank=True)  # blog|directory|social|user|agent
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


# A verification to qualify a `Candidate` as a `Spot`
class Verification(BaseModel):

    class Actions(models.TextChoices):
        APPROVE = "approve", _("Approve")
        REJECT = "reject", _("Reject")
        MERGE = "merge", _("Merge")
        EDIT = "edit", _("Edit")

    candidate   = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="verifications")
    action      = models.CharField(choices= Actions.choices, max_length=10)
    notes       = models.TextField(blank=True)
    by_user  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)



# V2 - Submission (To Preserve raw user/agent form separate from Candidate)
# class Submission(BaseModel):
#     id (PK)
#     payload (jsonb) ⟶ the unprocessed body
#     candidate_id? (FK) ⟶ link once normalized
#     submitted_by_email? (text)