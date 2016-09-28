# admin.py - MetroNetworkService Django Admin

from core.admin import ReadOnlyAwareAdmin
from core.admin import XOSBaseAdmin
from django.contrib import admin
from django import forms
from services.metronetwork.models import *


class MetroNetworkSystemAdmin(ReadOnlyAwareAdmin):
    model = MetroNetworkSystem
    verbose_name = "MetroNetwork System"
    verbose_name_plural = "MetroNetwork System"
    list_display = ("name", "administrativeState")
    list_display_links = ('name',)
    fieldsets = [(None, {
        'fields': ['name', 'administrativeState', 'description'],
        'classes': ['suit-tab suit-tab-general']})]

class NetworkDeviceAdminForm(forms.ModelForm):

    password = forms.CharField(required=False, widget = forms.PasswordInput(render_value=True))

    class Meta:
        model = NetworkDevice
        fields = '__all__'


class NetworkDeviceAdmin(XOSBaseAdmin):
    verbose_name = "Network Device"
    verbose_name_plural = "Network Devices"
    form = NetworkDeviceAdminForm
    list_display = ('id', 'restCtrlUrl', 'administrativeState', 'username')
    list_display_links = ('id', 'restCtrlUrl', 'administrativeState', 'username')

    fields = ('id', 'restCtrlUrl', 'administrativeState', 'username', 'password')

class NetworkEdgePortAdmin(XOSBaseAdmin):
    verbose_name = "Network Edge Port"
    verbose_name_plural = "Network Edge Ports"
    list_display = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir', 'name', 'location', 'latlng')
    list_display_links = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir')

    fields = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir', 'name', 'location', 'latlng')
    readonly_fields = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir')

class NetworkEdgeToEdgePointConnectionAdmin(XOSBaseAdmin):
    verbose_name = "Metro Network E-Line Service"
    verbose_name_plural = "Metro Network E-Line Services"
    list_display = ('id', 'sid', 'type', 'uni1', 'uni2', 'adminstate', 'operstate')
    list_display_links = ('id', 'sid', 'type', 'uni1', 'uni2', 'adminstate', 'operstate')

    fields = ('id', 'sid', 'type', 'uni1', 'uni2', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'type', 'uni1', 'uni2', 'operstate', 'backend_status')

class NetworkMultipointToMultipointConnectionAdmin(XOSBaseAdmin):
    verbose_name = "Metro Network E-LAN Service"
    verbose_name_plural = "Metro Network E-LAN Services"
    list_display = ('id', 'sid', 'type', 'adminstate', 'operstate')
    list_display_links = ('id', 'sid', 'type', 'adminstate', 'operstate')

    fields = ('id', 'sid', 'type', 'eps', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'sid', 'type', 'eps', 'adminstate', 'operstate', 'backend_status')

class NetworkEdgeToMultipointConnectionAdmin(XOSBaseAdmin):
    verbose_name = "Metro Network E-Tree Service"
    verbose_name_plural = "Metro Network E-Tree Services"
    list_display = ('id', 'sid', 'type', 'adminstate', 'operstate')
    list_display_links = ('id', 'sid', 'type', 'adminstate', 'operstate')

    fields = ('id', 'sid', 'type', 'root', 'eps', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'sid', 'type', 'root', 'eps', 'adminstate', 'operstate', 'backend_status')

admin.site.register(MetroNetworkSystem, MetroNetworkSystemAdmin)
admin.site.register(NetworkDevice, NetworkDeviceAdmin)
admin.site.register(NetworkEdgePort, NetworkEdgePortAdmin)
admin.site.register(NetworkEdgeToEdgePointConnection, NetworkEdgeToEdgePointConnectionAdmin)
admin.site.register(NetworkMultipointToMultipointConnection, NetworkMultipointToMultipointConnectionAdmin)
admin.site.register(NetworkEdgeToMultipointConnection, NetworkEdgeToMultipointConnectionAdmin)
