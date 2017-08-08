
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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
    list_display = ('id', 'name', 'sid', 'type', 'vlanid', 'uni1', 'uni2', 'adminstate', 'operstate')
    list_display_links = ('id', 'name', 'sid', 'type', 'vlanid', 'uni1', 'uni2', 'adminstate', 'operstate')

    fields = ('id', 'name', 'sid', 'type', 'vlanid', 'uni1', 'uni2', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'sid', 'backend_status')

class NetworkMultipointToMultipointConnectionAdmin(XOSBaseAdmin):
    verbose_name = "Metro Network E-LAN Service"
    verbose_name_plural = "Metro Network E-LAN Services"
    list_display = ('id', 'name', 'sid', 'type', 'vlanid', 'adminstate', 'operstate')
    list_display_links = ('id', 'name', 'sid', 'type', 'vlanid', 'adminstate', 'operstate')

    fields = ('id', 'name', 'sid', 'type', 'vlanid', 'eps', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'sid', 'backend_status')

class NetworkEdgeToMultipointConnectionAdmin(XOSBaseAdmin):
    verbose_name = "Metro Network E-Tree Service"
    verbose_name_plural = "Metro Network E-Tree Services"
    list_display = ('id', 'name', 'sid', 'type', 'vlanid', 'adminstate', 'operstate')
    list_display_links = ('id', 'name', 'sid', 'type', 'vlanid', 'adminstate', 'operstate')

    fields = ('id', 'name', 'sid', 'type', 'vlanid', 'root', 'eps', 'adminstate', 'operstate', 'backend_status')
    readonly_fields = ('id', 'sid', 'backend_status')

class RemotePortAdmin(XOSBaseAdmin):
    verbose_name = "Remote Port"
    verbose_name_plural = "Remote Ports"
    list_display = ('name', 'remoteportsite', 'edgeport')
    list_display_links = ('name', 'remoteportsite', 'edgeport')

    fields = ('name', 'remoteportsite', 'edgeport')

class BandwidthProfileAdmin(XOSBaseAdmin):
    verbose_name = "Bandwidth Profile"
    verbose_name_plural = "Bandwidth Profiles"
    list_display = ('bwpcfgcbs', 'bwpcfgebs', 'bwpcfgcir', 'bwpcfgeir', 'name')
    list_display_links = ('bwpcfgcbs', 'bwpcfgebs', 'bwpcfgcir', 'bwpcfgeir', 'name')

    fields = ('bwpcfgcbs', 'bwpcfgebs', 'bwpcfgcir', 'bwpcfgeir', 'name')

class ServiceSpokeAdmin(XOSBaseAdmin):
    verbose_name = "Service Spoke"
    verbose_name_plural = "Service Spokes"
    list_display = ('name','vnodlocalsite', 'remotesubscriber', 'adminstate', 'operstate', 'autoattached')
    list_display_links = ('name','vnodlocalsite', 'remotesubscriber', 'adminstate', 'operstate', 'autoattached')

    fields = ('name', 'id','vnodlocalsite', 'vnodlocalport', 'remotesubscriber', 'adminstate', 'operstate', 'backend_status', 'autoattached')
    readonly_fields = ('id', 'remotesubscriber', 'adminstate', 'operstate', 'backend_status')

class VnodGlobalServiceAdmin(XOSBaseAdmin):
    verbose_name = "VNOD Global Service"
    verbose_name_plural = "VNOD Global Services"
    list_display = ('servicehandle', 'vlanid', 'type','operstate', 'adminstate')
    list_display_links = ('servicehandle', 'vlanid', 'type','operstate', 'adminstate')

    fields = (
        'id', 'servicehandle', 'vlanid', 'type', 'metronetworkmultipoint', 'metronetworkpointtopoint', 'metronetworkroottomultipoint', 'operstate', 'adminstate', 'spokes', 'bandwidthProfile')
    readonly_fields = (
        'id', 'operstate', 'backend_status', 'metronetworkmultipoint', 'metronetworkpointtopoint', 'metronetworkroottomultipoint')

admin.site.register(MetroNetworkSystem, MetroNetworkSystemAdmin)
admin.site.register(NetworkDevice, NetworkDeviceAdmin)
admin.site.register(NetworkEdgePort, NetworkEdgePortAdmin)
admin.site.register(NetworkEdgeToEdgePointConnection, NetworkEdgeToEdgePointConnectionAdmin)
admin.site.register(NetworkMultipointToMultipointConnection, NetworkMultipointToMultipointConnectionAdmin)
admin.site.register(NetworkEdgeToMultipointConnection, NetworkEdgeToMultipointConnectionAdmin)
admin.site.register(BandwidthProfile, BandwidthProfileAdmin)
admin.site.register(ServiceSpoke, ServiceSpokeAdmin)
admin.site.register(VnodGlobalService, VnodGlobalServiceAdmin)
admin.site.register(RemotePort, RemotePortAdmin)




