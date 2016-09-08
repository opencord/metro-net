# admin.py - MetroNetworkService Django Admin

from core.admin import ReadOnlyAwareAdmin
from core.admin import XOSBaseAdmin
from django.contrib import admin
from django import forms
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

class NetworkDeviceAdminForm(forms.ModelForm):

    password = forms.CharField(required=False, widget = forms.PasswordInput(render_value=True))

    class Meta:
        model = NetworkDevice
        fields = '__all__'


class NetworkDeviceAdmin(XOSBaseAdmin):

    form = NetworkDeviceAdminForm
    list_display = ('id', 'restCtrlUrl', 'administrativeState', 'username')
    list_display_links = ('id', 'restCtrlUrl', 'administrativeState', 'username')

    fields = ('id', 'restCtrlUrl', 'administrativeState', 'username', 'password')

class NetworkPortAdmin(XOSBaseAdmin):
    list_display = ('id', 'element')
    list_display_links = ('id', 'element')

    fields = ('id', 'element')
    readonly_fields = ('id', 'element')

class NetworkEdgePortAdmin(XOSBaseAdmin):
    list_display = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir', 'name', 'location', 'latlng')
    list_display_links = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir')

    fields = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir', 'name', 'location', 'latlng')
    readonly_fields = ('id', 'pid', 'element', 'bwpCfgCbs', 'bwpCfgEbs', 'bwpCfgCir', 'bwpCfgEir')


class NetworkInterLinkAdmin(XOSBaseAdmin):
    list_display = ('discovery', 'src', 'dest', 'state')
    list_display_links = ('discovery', 'src', 'dest', 'state')

    fields = ('discovery', 'src', 'dest', 'state')
    readonly_fields = ('discovery', 'src', 'dest', 'state')

class NetworkPointToPointConnectionAdmin(XOSBaseAdmin):
    list_display = ('id', 'sid', 'type', 'src', 'dest', 'adminstate', 'operstate')
    list_display_links = ('id', 'sid', 'type', 'src', 'dest', 'adminstate', 'operstate')

    fields = ('id', 'sid', 'type', 'src', 'dest', 'adminstate', 'operstate')
    readonly_fields = ('id', 'type', 'src', 'dest', 'operstate')

class NetworkEdgePointToEdgePointConnectionAdmin(XOSBaseAdmin):
    list_display = ('id', 'sid', 'type', 'uni1', 'uni2', 'adminstate', 'operstate')
    list_display_links = ('id', 'sid', 'type', 'uni1', 'uni2', 'adminstate', 'operstate')

    fields = ('id', 'sid', 'type', 'uni1', 'uni2', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'type', 'uni1', 'uni2', 'operstate', 'backend_status')

class NetworkMultipointConnectionAdmin(XOSBaseAdmin):
    list_display = ('type', 'state')
    list_display_links = ('type', 'state')

    fields = ('type', 'eps', 'state')
    readonly_fields = ('type', 'eps', 'state')

admin.site.register(MetroNetworkService, MetroServiceAdmin)
admin.site.register(NetworkDevice, NetworkDeviceAdmin)
admin.site.register(NetworkPort, NetworkPortAdmin)
admin.site.register(NetworkEdgePort, NetworkEdgePortAdmin)
admin.site.register(NetworkInterLink, NetworkInterLinkAdmin)
admin.site.register(NetworkPointToPointConnection, NetworkPointToPointConnectionAdmin)
admin.site.register(NetworkEdgeToEdgePointConnection, NetworkEdgePointToEdgePointConnectionAdmin)
admin.site.register(NetworkMultipointConnection, NetworkMultipointConnectionAdmin)
