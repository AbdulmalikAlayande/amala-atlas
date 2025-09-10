
from django.contrib import admin

from places.models import Candidate, Spot, Verification


# Register your models here.
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'raw_address', 'score', 'lat', 'lng', 'city', 'country', 'status')

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lng', 'address', 'city', 'state', 'country', 'zipcode')

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'action', 'notes')