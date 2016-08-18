# admin.py - MetroNetworkService Django Admin

from core.admin import ReadOnlyAwareAdmin
from django.contrib import admin
from services.metronetwork.models import *


class MetroServiceAdmin(ReadOnlyAwareAdmin):
    model = MetroNetworkService
    verbose_name = "MetroNetwork Service"
    verbose_name_plural = "MetroNetwork Services"
    list_display = ("name", "administrativeState")
    list_display_links = ('name',)
    fieldsets = [(None, {
        'fields': ['name', 'administrativeState', 'description'],
        'classes': ['suit-tab suit-tab-general']})]


admin.site.register(MetroNetworkService, MetroServiceAdmin)
