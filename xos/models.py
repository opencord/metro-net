# models.py -  Metro Network Service

from django.db import models
from core.models import Service
from core.models import PlCoreBase
from core.models import Site

METRONETWORK_KIND = "metronetwork"
SERVICE_NAME = 'metronetwork'
SERVICE_NAME_ELINE_VERBOSE = 'E-Line Service'
SERVICE_NAME_ELAN_VERBOSE = 'E-LAN Service'
SERVICE_NAME_ETREE_VERBOSE = 'E-Tree Service'

class MetroNetworkSystem(PlCoreBase):

    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "Metro Network System"

    ADMINISTRATIVE_STATE = (
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled')
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    name = models.CharField(unique=True,
                           verbose_name="Name",
                           max_length=256,
                           editable=True)

    description = models.CharField(verbose_name="Description",
                                   max_length=1024,
                                   editable=True)

    restUrl = models.CharField(verbose_name="Rest URL",
                               max_length=256,
                               editable=True)

    administrativeState = models.CharField(choices=ADMINISTRATIVE_STATE,
                                           default='disabled',
                                           verbose_name="AdministrativeState",
                                           max_length=16,
                                           editable=True)

    operationalState = models.CharField(choices=OPERATIONALSTATE,
                                        verbose_name="OperationalState",
                                        max_length=256,
                                        editable=True)

    def __init__(self, *args, **kwargs):
        super(MetroNetworkSystem, self).__init__(*args, **kwargs)

    def getAdminstrativeState(self):
         return self.administrativeState

    def setAdminstrativeState(self, value):
        self.administrativeState = value

    def getOperationalState(self):
        return self.operationalState

    def getRestUrl(self):
        return self.restUrl


class NetworkDevice(PlCoreBase):

    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "Network Device"

    ADMINISTRATIVE_STATE = (
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
        ('syncrequested', 'SyncRequested'),
        ('syncinprogress', 'SyncInProgress')
    )

    AUTH_TYPE = (
        ('basic', 'Basic'),
        ('key', 'Key'),
        ('oauth', 'OAuth')
    )

    # Leaving out the attributes below for now - not clear we will need them
    # type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=False)
    # manufacturer = models.CharField(unique=False, verbose_name="Manufacturer", max_length=256, editable=False)
    # serialNumber = models.CharField(unique=True, verbose_name="Serial Number", max_length=256, editable=False)
    # chassisId = models.CharField(unique=False, verbose_name="Chassis ID", max_length=256, editable=False)

    name = models.CharField(max_length=20, help_text="Device friendly name", null=True, blank=True)
    restCtrlUrl = models.CharField(unique=True,
                               verbose_name="RestCtrlURL",
                               max_length=256,
                               editable=True)
    authType = models.CharField(choices=AUTH_TYPE, verbose_name='Auth Type', max_length=16, editable=True)
    username = models.CharField(verbose_name='Username', max_length=32, editable=True, blank=True)
    password = models.CharField(max_length=32, verbose_name='Password', editable=True, blank=True)
    administrativeState = models.CharField(choices=ADMINISTRATIVE_STATE,
                                           default='disabled',
                                           verbose_name="AdministrativeState",
                                           max_length=16,
                                           editable=True)
    id = models.CharField(unique=True,
                          verbose_name="Element Id",
                          primary_key=True,
                          max_length=256,
                          editable=True)

    def __init__(self, *args, **kwargs):
        super(NetworkDevice, self).__init__(*args, **kwargs)

class NetworkEdgePort(PlCoreBase):

    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "Network Edge Port"

    element = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE)
    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    pid = models.CharField(unique=True, verbose_name="Port ID", max_length=256, editable=False)
    bwpCfgCbs = models.IntegerField(verbose_name="Committed Burst Size", editable=False, blank=True)
    bwpCfgEbs = models.IntegerField(verbose_name="Excess Burst Size", editable=False, blank=True)
    bwpCfgCir = models.IntegerField(verbose_name="Committed Information Rate", editable=False, blank=True)
    bwpCfgEir = models.IntegerField(verbose_name="Excess Information Rate", editable=False, blank=True)
    name = models.CharField(verbose_name="Name", max_length=256, editable=True, blank=True)
    location = models.CharField(verbose_name="Location", max_length=256, editable=True, blank=True)
    latlng = models.CharField(verbose_name="Latitude/Longitude", max_length=50, editable=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(NetworkEdgePort, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.pid)

    def save(self, *args, **kwargs):

        if self.latlng:
            try:
                latlng_value = getattr(self, 'latlng').strip()
                if (latlng_value.startswith('[') and latlng_value.endswith(']') and latlng_value.index(',') > 0):
                    lat = latlng_value[1: latlng_value.index(',')].strip()
                    lng = latlng_value[latlng_value.index(',') + 1: len(latlng_value) - 1].strip()

                    #If lat and lng are not floats, the code below should result in an error.
                    lat_validation = float(lat)
                    lng_validation = float(lng)
                else:
                    raise ValueError("The lat/lng value is not formatted correctly.")
            except:
                raise ValueError("The lat/lng value is not formatted correctly.")

        super(NetworkEdgePort, self).save(*args, **kwargs)

#E-Line Service
class NetworkEdgeToEdgePointConnection(Service):

    class Meta:
        app_label = SERVICE_NAME
        verbose_name = SERVICE_NAME_ELINE_VERBOSE

    TYPE = (
        ('direct', 'Direct'),
        ('tunnel', 'Tunnel'),
        ('optical', 'Optical'),
        ('virtual', 'Virtual'),
        ('Point_To_Point', 'Point To Point')
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVESTATE = (
        ('disabled', 'Disabled'),
        ('activationrequested', 'ActivationRequested'),
        ('enabled', 'Enabled'),
        ('invalid', 'Invalid'),
        ('deactivationrequested', 'DeactivationRequested')
    )

    sid = models.CharField(verbose_name="Service ID", max_length=256, editable=True, blank=True)
    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=True)
    vlanid = models.CharField(verbose_name="Vlanid", max_length=64, editable=True)
    uni1 = models.ForeignKey(NetworkEdgePort,
                            related_name='EdgePointToEdgePointSrc',
                            verbose_name="UNI 1",
                            editable=True,
                            on_delete=models.CASCADE)
    uni2 = models.ForeignKey(NetworkEdgePort,
                             related_name='EdgePointToEdgePointDst',
                             verbose_name="UNI 2",
                             editable=True,
                             on_delete=models.CASCADE)
    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256, editable=True)
    adminstate = models.CharField(choices=ADMINISTRATIVESTATE, verbose_name="AdministrativeState", max_length=256, editable=True)

    #uni1_createbuffer = models.CharField(max_length=256, default="{}", null=True)
    #uni2_createbuffer = models.CharField(max_length=256, default="{}", null=True)

    def __init__(self, *args, **kwargs):
        super(NetworkEdgeToEdgePointConnection, self).__init__(*args, **kwargs)

#E-Tree Service
class NetworkEdgeToMultipointConnection(Service):

    class Meta:
        app_label = SERVICE_NAME
        verbose_name = SERVICE_NAME_ETREE_VERBOSE

    TYPE = (
        ('vlan', 'VLAN'),
        ('ip', 'IP'),
        ('ethernet', 'Ethernet'),
        ('Root_Multipoint', 'Root Multipoint')
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVESTATE = (
        ('disabled', 'Disabled'),
        ('activationrequested', 'ActivationRequested'),
        ('enabled', 'Enabled'),
        ('invalid', 'Invalid'),
        ('deactivationrequested', 'DeactivationRequested')
    )

    sid = models.CharField(verbose_name="Service ID", max_length=256, editable=True, blank=True)
    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=True)
    vlanid = models.CharField(verbose_name="Vlanid", max_length=64, editable=True)
    root = models.ForeignKey(NetworkEdgePort,
                            related_name='EdgeToMultipointRoot',
                            verbose_name="Root",
                            editable=True,
                            on_delete=models.CASCADE)
    eps = models.ManyToManyField(NetworkEdgePort,
                                 related_name='%(class)s_eps',
                                 verbose_name="Endpoints",
                                 editable=True)
    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256,
                                 editable=True)
    adminstate = models.CharField(choices=ADMINISTRATIVESTATE, verbose_name="AdministrativeState", max_length=256,
                                  editable=True)

    # Scratch Area to help deal with the Many to Many relationship with the eps
    #eps_createbuffer = models.CharField(max_length=1024, default="{}", null=True)

    def __init__(self, *args, **kwargs):
        super(NetworkEdgeToMultipointConnection, self).__init__(*args, **kwargs)

#E-LAN Service
class NetworkMultipointToMultipointConnection(Service):

    class Meta:
        app_label = SERVICE_NAME
        verbose_name = SERVICE_NAME_ELAN_VERBOSE

    TYPE = (
        ('vlan', 'VLAN'),
        ('ip', 'IP'),
        ('ethernet', 'Ethernet'),
        ('Multipoint_To_Multipoint', 'Multipoint To Multipoint')
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVESTATE = (
        ('disabled', 'Disabled'),
        ('activationrequested', 'ActivationRequested'),
        ('enabled', 'Enabled'),
        ('invalid', 'Invalid'),
        ('deactivationrequested', 'DeactivationRequested')
    )

    sid = models.CharField(verbose_name="Service ID", max_length=256, editable=True, blank=True)
    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=True)
    vlanid = models.CharField(verbose_name="Vlanid", max_length=64, editable=True)
    eps = models.ManyToManyField(NetworkEdgePort,
                                 related_name='%(class)s_eps',
                                 verbose_name="Endpoints",
                                 editable=True)

    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256,
                                 editable=True)
    adminstate = models.CharField(choices=ADMINISTRATIVESTATE, verbose_name="AdministrativeState", max_length=256,
                              editable=True)

    # Scratch Area to help deal with the Many to Many relationship with the eps
    #eps_createbuffer = models.CharField(max_length=1024, default="{}", null=True)

    def __init__(self, *args, **kwargs):
        super(NetworkMultipointToMultipointConnection, self).__init__(*args, **kwargs)

class BandwidthProfile(PlCoreBase):

    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "Bandwidth Profile"

    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    bwpcfgcbs = models.IntegerField(verbose_name="Committed Burst Size", editable=True)
    bwpcfgebs = models.IntegerField(verbose_name="Excess Burst Size", editable=True)
    bwpcfgcir = models.IntegerField(verbose_name="Committed Information Rate", editable=True)
    bwpcfgeir = models.IntegerField(verbose_name="Excess Information Rate", editable=True)
    name = models.CharField(unique=True, verbose_name="Name", max_length=256, editable=True)

    def __init__(self, *args, **kwargs):
        super(BandwidthProfile, self).__init__(*args, **kwargs)

    def __unicode__(self):  return u'%s' % (self.name)

# VNoD Global Objects - model is included in metro-net for simplicity

class RemotePort(PlCoreBase):
    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "Remote Port"

    remoteportsite = models.ForeignKey(Site,
                                       related_name='RemotePortSite',
                                       verbose_name="RemotePortSite",
                                       editable=True,
                                       on_delete=models.CASCADE)

    edgeport = models.ForeignKey(NetworkEdgePort,
                                 related_name='RemotePortEdgePort',
                                 verbose_name="RemotePortEdgePort",
                                 editable=True,
                                 on_delete=models.CASCADE)

    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    name = models.CharField(unique=True, verbose_name="Name", max_length=256, editable=True)

    def __init__(self, *args, **kwargs):
        super(RemotePort, self).__init__(*args, **kwargs)

    def __unicode__(self):  return u'%s' % (self.name)

class ServiceSpoke(PlCoreBase):

    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "Service Spoke"

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVE_STATE = (
        ('disabled', 'Disabled'),
        ('configured', 'Configured'),
        ('impaired', 'Impaired'),
        ('enabled', 'Enabled')
    )

    vnodlocalsite = models.ForeignKey(Site,
                      related_name='VnodLocalSite',
                      verbose_name="VnodLocalSite",
                      editable=True,
                      on_delete=models.CASCADE)

    vnodlocalport = models.ForeignKey(RemotePort,
                                      related_name='VnodLocalPort',
                                      verbose_name="VnodLocalPort",
                                      editable=True,
                                      on_delete=models.CASCADE)

    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    name = models.CharField(unique=True, verbose_name="Name", max_length=256, editable=True)
    remotesubscriber = models.CharField(verbose_name="RemoteSubscriber", max_length=256, blank=True, editable=False)
    remotevnodid = models.CharField(verbose_name="RemoteVnodId", max_length=256, blank=True, editable=False)
    autoattached = models.BooleanField(verbose_name="Auto-Attached", default=False, editable=True)
    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256,
                                 editable=True, default='inactive')
    adminstate = models.CharField(choices=ADMINISTRATIVE_STATE, default='disabled', verbose_name="AdministrativeState",
                                           max_length=64, editable=True)

    def __init__(self, *args, **kwargs):
        super(ServiceSpoke, self).__init__(*args, **kwargs)

    def __unicode__(self):  return u'%s' % (self.name)

class VnodGlobalService(Service):

    class Meta:
        app_label = SERVICE_NAME
        verbose_name = "Virtual Network On Demand Global Service"

    TYPE = (
        ('eline', SERVICE_NAME_ELINE_VERBOSE),
        ('elan', SERVICE_NAME_ELAN_VERBOSE),
        ('etree', SERVICE_NAME_ETREE_VERBOSE),
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVESTATE = (
        ('disabled', 'Disabled'),
        ('activationrequested', 'ActivationRequested'),
        ('enabled', 'Enabled'),
        ('invalid', 'Invalid'),
        ('deactivationrequested', 'DeactivationRequested')
    )

    servicehandle = models.CharField(unique=True, verbose_name="Servicehandle", max_length=64, editable=True)
    vlanid = models.CharField(verbose_name="Vlanid", max_length=64, editable=True)
    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=True)

    metronetworkroottomultipoint = models.ForeignKey(NetworkEdgeToMultipointConnection,
                            related_name='EtreeService',
                            verbose_name="EtreeService",
                            null=True,
                            editable=True,
                            on_delete=models.CASCADE)

    metronetworkmultipoint = models.ForeignKey(NetworkMultipointToMultipointConnection,
                                                     related_name='ElanService',
                                                     verbose_name="ElanService",
                                                     null=True,
                                                     editable=True,
                                                     on_delete=models.CASCADE)

    metronetworkpointtopoint = models.ForeignKey(NetworkEdgeToEdgePointConnection,
                                               related_name='ElineService',
                                               verbose_name="ElineService",
                                               null=True,
                                               editable=True,
                                               on_delete=models.CASCADE)

    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256,
                                 editable=True)

    adminstate = models.CharField(choices=ADMINISTRATIVESTATE, verbose_name="AdministrativeState", max_length=256,
                                  editable=True, default='enabled')

    spokes = models.ManyToManyField(ServiceSpoke,
                                 related_name='ServiceSpokes',
                                 verbose_name="Spokes",
                                 editable=True)

    bandwidthProfile = models.ForeignKey(BandwidthProfile,
                                               related_name='BandwidthProfile',
                                               verbose_name="BandwidthProfile",
                                               editable=True,
                                               on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super(VnodGlobalService, self).__init__(*args, **kwargs)


class UserNetworkInterface(PlCoreBase):

    class Meta:
        app_label = METRONETWORK_KIND
        verbose_name = "User Network Interface"

    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    enabled = models.IntegerField(verbose_name="State of UNI", editable=True)
    capacity = models.IntegerField(verbose_name="UNI Capacity", editable=True)
    bw_used = models.IntegerField(verbose_name="UNI bandwidth used", editable=True)
    vlanIds = models.CharField(verbose_name="VlanIds in this UNI", max_length=256, editable=True)
    location = models.CharField(verbose_name="Location", max_length=256, editable=True, blank=True)
    latlng = models.CharField(verbose_name="Latitude/Longitude", max_length=50, editable=True, blank=True)
    name = models.CharField(unique=True, verbose_name="Name", max_length=256, editable=True)

    def __init__(self, *args, **kwargs):
        super(UserNetworkInterface, self).__init__(*args, **kwargs)

    def __unicode__(self):  return u'%s' % (self.name)

    def save(self, *args, **kwargs):

        if self.latlng:
            try:
                latlng_value = getattr(self, 'latlng').strip()
                if (latlng_value.startswith('[') and latlng_value.endswith(']') and latlng_value.index(',') > 0):
                    lat = latlng_value[1: latlng_value.index(',')].strip()
                    lng = latlng_value[latlng_value.index(',') + 1: len(latlng_value) - 1].strip()

                    # If lat and lng are not floats, the code below should result in an error.
                    lat_validation = float(lat)
                    lng_validation = float(lng)
                else:
                    raise ValueError("The lat/lng value is not formatted correctly.")
            except:
                raise ValueError("The lat/lng value is not formatted correctly.")

        super(UserNetworkInterface, self).save(*args, **kwargs)