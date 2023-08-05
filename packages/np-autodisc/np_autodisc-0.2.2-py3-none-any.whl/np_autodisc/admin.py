# admin.py

from django.contrib import admin
from .models import DiscoveryRequest

@admin.register(DiscoveryRequest)
class DiscReqAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'job')
