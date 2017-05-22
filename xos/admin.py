# admin.py - MetroNetworkService Django Admin

from core.admin import ReadOnlyAwareAdmin
from core.admin import XOSBaseAdmin
from django.contrib import admin
from django import forms


class XOSMetronetBandwithProfileAdmin(XOSBaseAdmin):
    verbose_name = "Bandwidth Profile"
    list_display = ('cbs','ebs','cir','eir','name')

    fields = ('cbs', 'ebs', 'cir', 'eir', 'name')

class XOSMetronetUNIAdmin(XOSBaseAdmin):
    verbose_name = "User Network Interface"
    list_display = ('tenant', 'vlanIds', 'cpe_id', 'latlng', 'name')
    fields = ('tenant','vlanIds', 'cpe_id', 'latlng', 'name')

class XOSMetronetEnterpriseLocationAdmin(XOSBaseAdmin):
    verbose_name = "Enterprise Location"
    list_display = ('name', 'cord_site_ip', 'cord_site_port', 'cord_site_username', 'cord_site_password', 'cord_site_type')
    fields = ('name', 'cord_site_ip', 'cord_site_port', 'cord_site_username', 'cord_site_password', 'cord_site_type')

class XOSMetronetOnosModelAdmin(XOSBaseAdmin):
    verbose_name = "Open Network Operating System"
    list_display = ('name', 'onos_ip', 'onos_port', 'onos_username', 'onos_password', 'onos_type')
    fields = ('name', 'onos_ip', 'onos_port', 'onos_username', 'onos_password', 'onos_type')

class XOSMetronetELineAdmin(XOSBaseAdmin):
    verbose_name = "Ethernet Virtual Private Line"
    list_display = ('name', 'connect_point_1_id', 'connect_point_2_id', 'vlanids', 'cord_site_name', 'bwp')
    fields = ('name', 'connect_point_1_id', 'connect_point_2_id', 'vlanids', 'cord_site_name', 'bwp')

admin.site.register(XOSMetronetBandwithProfile, XOSMetronetBandwithProfileAdmin)
admin.site.register(XOSMetronetUNI, XOSMetronetUNIAdmin)
admin.site.register(XOSMetronetEnterpriseLocation, XOSMetronetEnterpriseLocationAdmin)
admin.site.register(XOSMetronetOnosModel, XOSMetronetOnosModelAdmin)
admin.site.register(XOSMetronetELine, XOSMetronetELineAdmin)